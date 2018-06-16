from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django.templatetags.static import static
from PIL import Image

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

def image(request, image=''):

    context = { 'image_id': image }
    return TemplateResponse(request, 'index.html', context)
