import qrcode
from PIL import Image
import base64
from io import BytesIO

DEF_SIZE_MARKER = 512

def create_qr_from_text(text):
    """
    Creates qr code.
    Args:
      *text* (str) text
    Out:
      PIL Image with QR code
    """
    qr = qrcode.QRCode(
     version=1,
     error_correction=qrcode.constants.ERROR_CORRECT_L,
     box_size=3,
     border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image()
    return img

def put_qr_on_marker(text, marker_in, marker_qr_out = 'markerqr.png'):
    """
    Puts qr code with text on marker image.
    Args:
      *text* (str) text
      *marker_in* - (str) - input png file
      *marker_qr_out* - (str) - output png  file
    """
    img = Image.open(marker_in)

    qr_img = create_qr_from_text(text)

    t_width = img.size[0]
    t_height = img.size[1]
    assert t_height == t_width == DEF_SIZE_MARKER, "marker size does not match ({0}, {0})".format(DEF_SIZE_MARKER)

    new_im = Image.new('RGB', (t_width, t_height), "white")

    new_im.paste(img, (0, 0))
    new_im.paste(qr_img, (80 +  qr_img.size[0], 155))

    buffered = BytesIO()
    new_im.save(buffered, format = "png")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str
