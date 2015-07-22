#-*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
POSTS_PER_PAGE = 7
SECRET_KEY = 'you-will-never-guess'
# SQLALCHEMY_ECHO = True

UPLOAD_DIRECTORY = os.path.join(basedir, 'upload')

DATABASE = 'logpot.db'
DATABASE_DIRECTORY = os.path.join(basedir, 'db')
DATABASE_PATH = os.path.join(DATABASE_DIRECTORY, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

LOG = 'logpot.log'
LOG_DIRECTORY = os.path.join(basedir, 'log')
LOG_PATH = os.path.join(LOG_DIRECTORY, LOG)
