#-*- coding: utf-8 -*-

from logpot.app import app
from flask import url_for, send_from_directory, redirect, request, make_response
import os


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
    path = '_settings/' + filename
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


from feedgen.feed import FeedGenerator
from logpot.entry.models import Entry
from logpot.ext import db
from dateutil import zoneinfo, tz
@app.route('/rss')
def rss():
    tz    = zoneinfo.gettz('Asia/Tokyo')
    title = app.config["site_title"]
    sub_title = app.config["site_subtitle"]
    link = request.url_root
    feed_link = request.url

    fg = FeedGenerator()
    fg.title(title)
    fg.description(sub_title)
    fg.link( href=link, rel='alternate' )
    fg.link( href=feed_link, rel='self' )
    fg.language('ja')

    entries = db.session.query(Entry).filter_by(is_published=True).outerjoin(Entry.category).order_by(Entry.id.desc())

    for entry in entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link( href=link + 'entry/' + entry.slug, rel='alternate' )
        fe.description(entry.body)
        fe.pubdate(entry.created_at.replace(tzinfo=tz))
        fe.category({'term': str(entry.category)})

    response = make_response(fg.rss_str(pretty=True))
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response
