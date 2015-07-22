#-*- coding: utf-8 -*-

from logpot.app import app
from flask import url_for, send_from_directory, redirect
import os


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


@app.route('/static/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/static/img/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/static/img/', filename)


@app.route('/static/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/bower_components/<path:filename>')
def bower(filename):
    return send_from_directory(app.root_path + '/static/bower_components/', filename)

@app.route('/_settings/<path:filename>')
def img_settings(filename):
    path = 'settings/' + filename
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], path)

@app.route('/entry/<path:slug>/<path:filename>')
def img_upload(slug, filename):
    path = slug + '/' + filename
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], path)

@app.route('/entry/<path:slug>/<path:filename>_thumb_s<path:ext>')
def img_upload_thumb_s(slug, filename, ext):
    path = slug + '/thumb/s/' + filename + ext
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], path)

@app.route('/entry/<path:slug>/<path:filename>_thumb_m<path:ext>')
def img_upload_thumb_m(slug, filename, ext):
    path = slug + '/thumb/m/' + filename + ext
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], path)

@app.route('/entry/<path:slug>/<path:filename>_thumb_l<path:ext>')
def img_upload_thumb_l(slug, filename, ext):
    path = slug + '/thumb/l/' + filename + ext
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], path)


@app.route('/')
def index():
    return redirect(url_for('entry.entries'))
