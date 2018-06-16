from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django.templatetags.static import static
from PIL import Image

def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):

    context = { 'image_id': image }

    return TemplateResponse(request, 'index.html', context)
