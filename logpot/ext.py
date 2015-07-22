#-*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()

loginManager = LoginManager()

migrate = Migrate()

debugtoolbar = DebugToolbarExtension()
