from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.request import urlopen
import base64
import os
from django.http import HttpResponse

from .utils import create_qr_from_text, put_qr_on_marker


def qr(request, image=''):

    qr_link = settings.BASE_URL + '/test/image'
    # qr_code = create_qr_from_text(qr_link)
    marker_with_qr = put_qr_on_marker(qr_link, 'staticfiles/img/marker.png')

    pillow_image = ContentFile(base64.b64decode(marker_with_qr), name='temp.jpg')

    return HttpResponse(pillow_image, content_type="image/jpeg")

def lh(request, image=''):
    lh_link = 'https://raw.githubusercontent.com/TimVanMourik/ChristmasAR/master/data/mni_left_hemisphere.dae'

    return HttpResponse(urlopen(lh_link), content_type='application/xml')

def rh(request, image=''):
    rh_link = 'https://raw.githubusercontent.com/TimVanMourik/ChristmasAR/master/data/mni_right_hemisphere.dae'

    return HttpResponse(urlopen(rh_link), content_type='application/xml')
