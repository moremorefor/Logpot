#-*- coding: utf-8 -*-

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
