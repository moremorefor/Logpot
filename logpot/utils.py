#-*- coding: utf-8 -*-

import os
import mimetypes
import math
import yaml
from PIL import Image

class ImageUtil():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

    def ratio(width, height):
        if width > height:
            ratio = float(height) / float(width)
        else:
            ratio = float(width) / float(height)
        return ratio

    def sanitize(value):
        value = int(value)
        if value > 300:
            value = 300
        return value

    @classmethod
    def crop_image(cls, image, size):
        current_width, current_height = image.size
        r = cls.ratio(current_width, current_height)

        if current_width > current_height:
            height = cls.sanitize(size)
            width = int(height / r)
        else:
            width = cls.sanitize(size)
            height = int(width / r)

        new_width, new_height = width, height
        left, top, right, bottom = 0, 0, new_width, new_height

        if new_width > new_height:
            left = (new_width - new_height) / 2
            if isinstance(left, float):
                left = math.ceil(left)
                right = new_width - (left - 1)
            else:
                right = new_width - left
        else:
            top = (new_height - new_width) / 2
            if isinstance(top, float):
                top = math.ceil(top)
                bottom = new_height - (top - 1)
            else:
                bottom = new_height - top

        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        image = image.crop((left, top, right, bottom))
        return image

    @classmethod
    def getFileExtention(cls, mimetype):
        ext = mimetypes.guess_extension(mimetype)
        if ext == ".jpe":
            ext = ".jpg"
            return ext
        elif ext is None:
            ext = '.jpg'
            return ext
        else:
            return ext

def getDirectoryPath(app, directory):
    dirpath = os.path.join(app.config['UPLOAD_DIRECTORY'], directory)
    if os.path.exists(dirpath):
        return dirpath
    else:
        os.makedirs(dirpath)
        return dirpath

def loadSiteConfig(app):
    configfile = os.path.join(app.root_path, 'config.yml')
    if os.path.exists(configfile):
        f = open(configfile, 'r')
        data = yaml.load(f)
        f.close()
    else:
        data = {}
        data["site_title"]          = "Logpot"
        data["site_subtitle"]       = "This is a simple blog system build with Flask."
        data["site_author"]         = "Logpot"
        data["enable_link_github"]  = False
        data["enable_profile_img"]  = False
        data["display_poweredby"]   = True
        saveSiteConfig(app, data)

    app.config['site_title']          = data['site_title']
    app.config['site_subtitle']       = data['site_subtitle']
    app.config['site_author']         = data['site_author']
    app.config['enable_link_github']  = data['enable_link_github']
    app.config['enable_profile_img']  = data['enable_profile_img']
    app.config['display_poweredby']   = data['display_poweredby']
    return data

def saveSiteConfig(app, data):
    configfile = os.path.join(app.root_path, 'config.yml')
    f = open(configfile, 'w')
    yaml.dump(
        data,
        f,
        encoding='utf8',
        allow_unicode=True,
        default_flow_style=False
    )
    f.close()
    return True
