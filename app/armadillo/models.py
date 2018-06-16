from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.request import urlopen
import urllib.request, json
import base64
import os
from django.http import HttpResponse
from urllib.request import urlopen
import nibabel as nib
from nibabel.freesurfer import io as fsio

from django.core.files.uploadedfile import InMemoryUploadedFile

from .utils import create_qr_from_text, put_qr_on_marker, color_func, fv_scalar_to_collada


def qr(request, image=''):
    qr_link = os.path.join(settings.BASE_URL, 'neurovault/'+ image)
    marker_with_qr = put_qr_on_marker(qr_link, 'staticfiles/img/marker.png')
    image = ContentFile(base64.b64decode(marker_with_qr), name='temp.jpg')
    return HttpResponse(image, content_type="image/jpeg")

def hemisphere(request, image='', hemisphere=''):
    # query neurovault image
    fileUrl = f"https://neurovault.org/api/images/{image}"
    try:
        with urllib.request.urlopen(fileUrl) as url:
            fileData = json.loads(url.read().decode())
    except (urllib.error.HTTPError, ValueError):
        fileData = None

    surface = fileData[f"surface_{hemisphere}_file"]
    with urllib.request.urlopen(surface) as response:
        gii = response.read().decode()

    if hemisphere not in ["left","right"]:
        print("BAD HEMI IN IMAGE FUNC")
        exit(1)
    elif hemisphere == "left":
        hemi_short = "lh"
    else:
        hemi_short = "rh"

    # THIS IS A COMPLETE HACK
    # TODO: remove this
    # with open("temp.func.gii","w") as f:
       # f.write(gii)
    scalars = nib.load( os.path.join(settings.BASE_DIR, f'staticfiles/fs/{hemi_short}.func.gii'))
    #scalars = nib.load(f'/neurovault/{image}/gifti/{hemisphere}')
    scalars = scalars.darrays[0].data
    fs_base = os.path.join(settings.BASE_DIR, 'staticfiles/fs/')

    verts,faces = fsio.read_geometry(\
      os.path.join(fs_base,"%s.pial" % hemi_short))

    bytestream = bytes(fv_scalar_to_collada(verts,faces,scalars).getvalue())
    a  = ContentFile(bytestream, f"{hemisphere}.dae")
    file = InMemoryUploadedFile(a, None, f"{hemisphere}.dae", 'application/xml', len(bytestream), None)
    return HttpResponse(file, content_type='application/xml')

def gifti(request, image='', hemisphere=''):

    # query neurovault image
    fileUrl = f"https://neurovault.org/api/images/{image}"
    try:
        with urllib.request.urlopen(fileUrl) as url:
            fileData = json.loads(url.read().decode())
    except (urllib.error.HTTPError, ValueError):
        fileData = None

    surface = fileData[f"surface_{hemisphere}_file"]

    return HttpResponse(urlopen(surface), content_type='application/xml')
