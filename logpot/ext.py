#-*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.debugtoolbar import DebugToolbarExtension

from flask.ext.admin import Admin
from logpot.admin.base import MyAdminIndexView

db = SQLAlchemy()

loginManager = LoginManager()

migrate = Migrate()

debugtoolbar = DebugToolbarExtension()

admin = Admin(
    name='Logpot',
    endpoint='admin',
    index_view=MyAdminIndexView(),
    template_mode='bootstrap3'
)
