#-*- coding: utf-8 -*-

from flask import Blueprint

bp = Blueprint('auth', __name__)

from logpot.auth import views
