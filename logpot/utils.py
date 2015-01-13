#-*- coding: utf-8 -*-

import random
import string

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])


def random_str(self, length=10):
    rs = ""
    for i in range(length):
        rs += random.choice(string.ascii_letters)
    return rs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


import uuid


def unique_id():
    return hex(uuid.uuid4().time)[2:-1]
