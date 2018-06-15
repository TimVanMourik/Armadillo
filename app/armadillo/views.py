from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
import urllib.request, json

def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):
    # query neurovault image
    fileUrl = f"https://neurovault.org/api/images/{image}"
    try:
        with urllib.request.urlopen(fileUrl) as url:
            fileData = json.loads(url.read().decode())
    except (urllib.error.HTTPError, ValueError):
        fileData = None

    # parse image

    # colour file
    # surface_left_file =  fileData['surface_left_file']
    # surface_right_file = fileData['surface_right_file']

    # if surface_left_file != None & surface_right_file != None


    context = {}
    return TemplateResponse(request, 'index.html', context)

def test(request):
    context = {}
    return TemplateResponse(request, 'test.html', context)
