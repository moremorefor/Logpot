#-*- coding: utf-8 -*-

import os

from PIL import Image

#=========================================
# Helper
#=========================================


def ratio(width, height):
    if width > height:
        ratio = float(height) / float(width)
    else:
        ratio = float(width) / float(height)
    return ratio


def sanitize(value):
    value = int(value)
    if value > 700:
        value = 700
    return value


def measurements(image, width=None, height=None):
    current_width, current_height = image.size
    r = ratio(current_width, current_height)

    if not width and not height:
        width = 150

    if width:
        width = sanitize(width)
        height = int(width * r)
    elif height:
        height = sanitize(height)
        width = int(height * r)

    return (width, height)


def getExtentionName(ext):
    if ext == '.jpg' or ext == '.jpeg':
        return 'JPEG'
    elif ext == '.png':
        return 'PNG'
    elif ext == 'gif':
        return 'GIF'


def getSaveDirectory(dirpath, thumb_size):
    save_path = os.path.join(dirpath, 'thumb', thumb_size)
    if os.path.exists(save_path):
        return save_path
    else:
        os.makedirs(save_path)
        return save_path


def createThumbnailImage(dirpath, filepath, thumb_size):
    img = Image.open(os.path.join(dirpath, filepath))
    if thumb_size == 's':
        size = measurements(img, width=150)
    elif thumb_size == 'm':
        size = measurements(img, width=300)
    elif thumb_size == 'l':
        size = measurements(img, width=450)
    else:
        size = measurements(img, width=150)
    filename, ext = os.path.splitext(filepath)
    ext = getExtentionName(ext)

    img.thumbnail(size, Image.ANTIALIAS)
    save_path = getSaveDirectory(dirpath, thumb_size)
    img.save(os.path.join(save_path, filepath), ext)
