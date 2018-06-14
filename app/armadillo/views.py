from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404

def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)
