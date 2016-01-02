#-*- coding: utf-8 -*-

from logpot.ext import db
from logpot.models import TimestampMixin


entry_tag = db.Table(
    'entry_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entries.id'))
)


class Entry(db.Model, TimestampMixin):

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    summary = db.Column(db.String(140), nullable=False)
    md_body = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String, unique=True, nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    #Many to One
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    author = db.relationship('User', backref='entries')
    category = db.relationship('Category', backref='entries')

    #Many to Many
    tags = db.relationship(
        'Tag', secondary=entry_tag, backref=db.backref('entries', lazy='dynamic')
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Entry %r>' % (self.title)


class Tag(db.Model, TimestampMixin):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # def __init__(self, name):
    #     self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag %r>' % (self.name)


class Category(db.Model, TimestampMixin):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Category %r>' % (self.name)
