import os


def delete_media(image):
    from shutil import rmtree
    from pathlib import Path
    randImgPath = image
    imgPath = Path(randImgPath.image.path)  # Get path of random image
    if os.path.isfile(imgPath):
        rmtree(imgPath.parent.parent)  # Delete parent of parent(media => Restaurant => name )
