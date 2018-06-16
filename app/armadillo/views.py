from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
import urllib.request, json
from urllib.request import urlopen
from django.templatetags.static import static
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

import nibabel as nib
from nibabel.freesurfer import io as fsio
import os
from django.conf import settings
import collada
import numpy as np

import io

def index(request):
    context = {}
    return TemplateResponse(request, 'welcome.html', context)

#todo: use matplotlib color functions
def color_func( scalars ):
    smin = np.min(scalars)
    smax = np.max(scalars)
    scalars = (scalars - smin) / smax
  
    colors = np.zeros((scalars.shape[0],3))
    colors[:,1] += scalars
    colors[:,2] += (1-scalars)
  
    return colors


def fv_scalar_to_collada(verts,faces,scalars):

    color = color_func(scalars)

    #create collada obj
    mesh = collada.Collada()

    #add shading
    effect = collada.material.Effect("effect0",\
      [], #TEXTURES GO HERE
      "phong", diffuse=(1,1,1), specular=(1,1,1),
      double_sided=True)
    mat = collada.material.Material("material0", "mymaterial", effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    vert_src = collada.source.FloatSource("verts-array", verts, ('X', 'Y', 'Z'))
    color_src = collada.source.FloatSource("colors-array", np.array(color), ('R', 'G', 'B'))

    geom = collada.geometry.Geometry(mesh, "geometry0", "fsave_test",\
      [vert_src,color_src])

    #creates list of inputs for collada DOM obj...so many decorators 
    input_list = collada.source.InputList()

    input_list.addInput(0, 'VERTEX', "#verts-array")
    input_list.addInput(1, 'COLOR', "#colors-array")

    #creates faces
    triset = geom.createTriangleSet(
      np.concatenate([faces,faces],axis=1),\
      input_list, "materialref")

    triset.generateNormals()

    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    #creates scene node, which causes display
    matnode = collada.scene.MaterialNode("materialref", mat, inputs=[])
    geomnode = collada.scene.GeometryNode(geom, [matnode])
    node = collada.scene.Node("node0", children=[geomnode])

    #create scene
    myscene = collada.scene.Scene("fs_base_scene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    buf = io.BytesIO()
    mesh.write(buf)
    return buf

def image(request, image='', hemi="left"):
    # query neurovault image
    fileUrl = f"https://neurovault.org/api/images/{image}"
    try:
        with urllib.request.urlopen(fileUrl) as url:
            fileData = json.loads(url.read().decode())
    except (urllib.error.HTTPError, ValueError):
        fileData = None

    if hemi not in ["left","right"]:
        print("BAD HEMI IN IMAGE FUNC")
        exit(1)
    elif hemi == "left":
        hemi_short = "lh"
    else:
        hemi_short = "rh"

    # parse image

    # colour file
    surface_file =  fileData['surface_%s_file' % hemi]

    with urllib.request.urlopen(surface_file) as response:
        gii = response.read()

    #THIS IS A COMPLETE HACK
    #TODO: remove this
    #with open("temp.func.gii","w") as f:
    #    f.write(gii)
    #scalars = nib.load("temp.func.gii")
    #gii_buf = io.BytesIO(bytes(gii))
    scalars = nib.load(gii)
    scalars = scalars.darrays[0].data
    ##print(lh_scalars.darrays[0].data)

    #nib.load("/neurovault/{image}/lh")

    fs_base = os.path.join(settings.BASE_DIR, 'staticfiles/fs/')
    verts,faces = fsio.read_geometry(\
      os.path.join(fs_base,"%s.pial" % hemi_short))

    return(fv_scalar_to_collada(verts,faces,scalars))

    # if surface_left_file != None & surface_right_file != None

    # create QR code
    # lh_link = urlresponse('https://raw.githubusercontent.com/TimVanMourik/ChristmasAR/master/data/mni_left_hemisphere.dae')
    # rh_link = ('https://raw.githubusercontent.com/TimVanMourik/ChristmasAR/master/data/mni_right_hemisphere.dae')
    # lh_file = InMemoryUploadedFile(lh_link, None, 'lh.dae', 'application/xml', os.path.getsize(lh_link), None)
    # rh_file = InMemoryUploadedFile(rh_link, None, 'rh.dae', 'application/xml', os.path.getsize(rh_link), None)


    # context = {'img_str': marker_with_qr}
    context = {
                'image_id': image,
              }

    return TemplateResponse(request, 'index.html', context)

def test(request, image=''):

    qr_link = settings.BASE_URL + '/test/image'
    # qr_code = create_qr_from_text(qr_link)
    marker_with_qr = put_qr_on_marker(qr_link, 'staticfiles/img/marker.png')

    pillow_image = ContentFile(base64.b64decode(marker_with_qr), name='temp.jpg')
    image_file = InMemoryUploadedFile(pillow_image, None, 'foo.jpg', 'image/jpeg', pillow_image.tell, None)



    # context = {'img_str': marker_with_qr}
    context = {
                'img_str': image_file.file,
              }

    return TemplateResponse(request, 'test.html', context)

    return HttpResponse(image_file, content_type="image/jpeg")
