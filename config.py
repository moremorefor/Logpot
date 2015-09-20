#-*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
POSTS_PER_PAGE = 7
SECRET_KEY = 'you-will-never-guess'

UPLOAD_DIRECTORY = os.path.join(basedir, 'upload')

SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/logpot'

LOG = 'logpot.log'
LOG_DIRECTORY = os.path.join(basedir, 'log')
LOG_PATH = os.path.join(LOG_DIRECTORY, LOG)
