#-*- coding: utf-8 -*-

from logpot.ext import db
from logpot.models import TimestampMixin

from passlib.hash import pbkdf2_sha256

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def generate_password_hash(self, password):
        return pbkdf2_sha256.encrypt(password)

    @classmethod
    def check_password_hash(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % (self.name)
