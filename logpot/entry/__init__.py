#-*- coding: utf-8 -*-

from flask import Blueprint

bp = Blueprint('entry', __name__)

from logpot.entry import views
