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

from .utils import create_qr_from_text, put_qr_on_marker


def qr(request, image=''):

    qr_link = settings.BASE_URL + 'neurovault/'+ image
    # qr_code = create_qr_from_text(qr_link)
    marker_with_qr = put_qr_on_marker(qr_link, 'staticfiles/img/marker.png')

    pillow_image = ContentFile(base64.b64decode(marker_with_qr), name='temp.jpg')

    return HttpResponse(pillow_image, content_type="image/jpeg")

def hemisphere(request, image='', hemisphere=''):
    link = f"https://raw.githubusercontent.com/TimVanMourik/ChristmasAR/master/data/mni_{hemisphere}_hemisphere.dae"

    return HttpResponse(urlopen(link), content_type='application/xml')

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
