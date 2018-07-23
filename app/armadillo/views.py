from django.template.response import TemplateResponse
import random

def index(request):
    neurovaultIds = [64604, 31997, 64605];
    context = {
                'randomImageId': random.choice(neurovaultIds),
                }
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):
    context = { 'image_id': image }
    return TemplateResponse(request, 'armadillo.html', context)
