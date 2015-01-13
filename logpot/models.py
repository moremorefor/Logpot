#-*- coding: utf-8 -*-

from logpot.ext import db

from sqlalchemy import event

import datetime


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)


@event.listens_for(TimestampMixin, 'before_insert', propagate=True)
def timestamp_before_insert(mapper, connection, target):
    now = datetime.datetime.now()
    target.created_at = now
    target.updated_at = now


@event.listens_for(TimestampMixin, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
