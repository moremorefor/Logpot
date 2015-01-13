#-*- coding: utf-8 -*-

import os

from flask import Flask, g
from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.admin.menu import MenuLink

from logpot.entry import bp as entry_bp
from logpot.auth import bp as auth_bp
from logpot.auth.models import User
from logpot.ext import db, loginManager, migrate, admin
from logpot.admin.image import ImageModelView
from logpot.admin.file import EntryFileView
from logpot.admin.user import UserModelView
from logpot.admin.entry import EntryModelView, CategoryModelView, TagModelView
from logpot.image.models import Image
from logpot.entry.models import Entry, Category, Tag


def create_app(config=None):
    app = Flask("logpot")

    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.config.from_object('config')  # pull in configuration

    CsrfProtect(app)

    # First, create a directory
    createDirectory(app)

    configure_blueprints(app)
    configure_extentions(app)
    configure_request_handler(app)
    configure_logging(app)

    return app


def configure_blueprints(app):
    app.register_blueprint(entry_bp, url_prefix='/entry')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def configure_extentions(app):
    db.init_app(app)

    loginManager.init_app(app)
    loginManager.login_view = 'auth.login'
    loginManager.login_message = 'Please log in!'

    @loginManager.user_loader
    def load_user(userid):
        return User.query.get(int(userid))

    migrate.init_app(app, db)

    # debugtoolbar.init_app(app)

    admin.init_app(app)
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(EntryModelView(Entry, db.session, endpoint='admin_entry', url='/admin/entry'))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_view(ImageModelView(Image, db.session, endpoint='admin_image', url='/admin/image'))
    admin.add_view(EntryFileView(app.config['UPLOAD_DIRECTORY']))
    admin.add_link(MenuLink(name='Back Home', url='/', category='Settings'))
    admin.add_link(MenuLink(name='Logout', endpoint='auth.logout', category='Settings'))


def configure_request_handler(app):
    @app.before_request
    def before_request():
        g.user = app

    @app.after_request
    def after_request(response):
        #whole application cache
        db.session.remove()
        return response


def configure_logging(app):
    from logging import Formatter, FileHandler
    handler = FileHandler(app.config["LOG_PATH"], encoding='utf8')
    handler.setFormatter(
        Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    app.logger.addHandler(handler)


def createDirectory(app):
    if not os.path.exists(app.config['UPLOAD_DIRECTORY']):
        os.makedirs(app.config['UPLOAD_DIRECTORY'])

    if not os.path.exists(app.config['LOG_DIRECTORY']):
        os.makedirs(app.config['LOG_DIRECTORY'])


app = create_app()
