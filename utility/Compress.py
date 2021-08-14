from io import BytesIO

from PIL import Image
from django.core.files import File


def compress_image(image, quality=70):
    img = Image.open(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_io = BytesIO()
    img.save(img_io, 'jpeg', quality=quality, optimize=True)
    new_image = File(img_io, name=image.name)
    return new_image
