from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django.templatetags.static import static
from PIL import Image

def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):

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
