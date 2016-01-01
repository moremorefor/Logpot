#-*- coding: utf-8 -*-

from flask import url_for
from logpot.ext import debugtoolbar
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_RECORD_QUERIES = True
    CSRF_ENABLED = True
    UPLOAD_DIRECTORY = os.path.join(basedir, 'upload')
    LOG = 'logpot.log'
    LOG_DIRECTORY = os.path.join(basedir, 'log')
    LOG_PATH = os.path.join(LOG_DIRECTORY, LOG)
    LOGPOT_POSTS_PER_PAGE = 7

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'logpot-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        debugtoolbar.init_app(app)

        @app.context_processor
        def override_url_for():
            return dict(url_for=dated_url_for)

        def dated_url_for(endpoint, **values):
            if endpoint == 'js_static':
                filename = values.get('filename', None)
                if filename:
                    file_path = os.path.join(app.root_path,
                                             'static/js', filename)
                    values['q'] = int(os.stat(file_path).st_mtime)
            elif endpoint == 'css_static':
                filename = values.get('filename', None)
                if filename:
                    file_path = os.path.join(app.root_path,
                                             'static/css', filename)
                    values['q'] = int(os.stat(file_path).st_mtime)
            return url_for(endpoint, **values)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'logpot.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
