#-*- coding: utf-8 -*-

from logpot.admin.base import AuthenticateView
from logpot.utils import ALLOWED_EXTENSIONS

from flask import flash, redirect
from flask.ext.admin import expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.babel import gettext

import os
import os.path as op
from operator import itemgetter
from datetime import datetime


class EntryFileView(AuthenticateView, FileAdmin):

    def __init__(self, dirpath, **kwargs):
        super().__init__(dirpath, **kwargs)
    can_delete = False
    can_upload = False
    can_mkdir = False
    allowed_extensions = ALLOWED_EXTENSIONS
