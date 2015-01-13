#-*- coding: utf-8 -*-

from logpot.ext import db
from logpot.models import TimestampMixin
from logpot.entry.models import Entry
from logpot.image.generate import createThumbnailImage

from flask import current_app
from sqlalchemy import event

import os
import os.path as op
import sys


class Image(db.Model, TimestampMixin):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)

    #Many to One
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'), nullable=False)
    entry = db.relationship('Entry', backref='images')

    def __repr__(self):
        return '<Image %r,%r,%r,%r>' % (self.id, self.name, self.path, self.entry_id)


@event.listens_for(Image, 'after_insert')
def create_thumbnail(mapper, connection, target):
    e = db.session.query(Entry).filter_by(id=target.entry_id).one()
    dirpath = op.join(current_app.config['UPLOAD_DIRECTORY'], e.slug)
    name, ext = op.splitext(target.path)
    try:
        createThumbnailImage(dirpath, target.path, 's')
        createThumbnailImage(dirpath, target.path, 'm')
        createThumbnailImage(dirpath, target.path, 'l')
    except:
        print("Unexpected error:", sys.exc_info()[0])


@event.listens_for(Image, 'after_delete')
def delete_images(mapper, connection, target):
    e = db.session.query(Entry).filter_by(id=target.entry_id).one()
    dirpath = op.join(current_app.config['UPLOAD_DIRECTORY'], e.slug)
    image_path = op.join(dirpath, target.path)
    thumb_s_path = op.join(dirpath, 'thumb', 's', target.path)
    thumb_m_path = op.join(dirpath, 'thumb', 'm', target.path)
    thumb_l_path = op.join(dirpath, 'thumb', 'l', target.path)
    try:
        os.remove(image_path)
        os.remove(thumb_s_path)
        os.remove(thumb_m_path)
        os.remove(thumb_l_path)
    except:
        print("Unexpected error:", sys.exc_info()[0])
