#-*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from logpot.entry.api import Heatmap

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(Heatmap, '/entry/heatmap', endpoint='entry-heatmap')
