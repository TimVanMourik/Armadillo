from django.template.response import TemplateResponse

def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):
    context = { 'image_id': image }
    return TemplateResponse(request, 'armadillo.html', context)
