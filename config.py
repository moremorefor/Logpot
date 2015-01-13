#-*- coding: utf-8 -*-

import os

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
DATABASE = 'tmp/logpot.db'
LOG = 'tmp/logpot.log'
CSRF_ENABLED = True
POSTS_PER_PAGE = 10
# SQLALCHEMY_ECHO = True

UPLOAD_DIRECTORY = os.path.join(basedir, 'upload')

DATABASE_PATH = os.path.join(basedir, DATABASE)
LOG_DIRECTORY = os.path.join(basedir, 'tmp')
LOG_PATH = os.path.join(basedir, LOG)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
