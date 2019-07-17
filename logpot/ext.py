#-*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()

loginManager = LoginManager()

migrate = Migrate()

debugtoolbar = DebugToolbarExtension()
