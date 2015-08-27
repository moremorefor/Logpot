#-*- coding: utf-8 -*-

from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileField
from wtforms import StringField, TextField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask.ext.admin.contrib.sqla.fields import QuerySelectField
from flask.ext.login import current_user

from logpot.ext import db
from logpot.entry.models import Entry

import re

class FileUploadForm(Form):
    uploadfile = FileField('image')
    name = StringField('Filename')
    entry_id = QuerySelectField(
        query_factory=lambda: db.session.query(Entry).filter_by(author=current_user).all()
    )

class SettingForm(Form):
    title              = StringField('Site title', validators=[DataRequired('Required field')])
    subtitle           = TextField('Site subtitle', validators=[DataRequired('Required field')])
    author             = StringField('Site author', validators=[DataRequired('Required field')])
    author_profile     = StringField('Author profile', validators=[DataRequired('Required field')])
    enable_link_github = BooleanField('Link author name to Github account')
    profile_img        = FileField('Profile image', validators=[])
    enable_profile_img = BooleanField('Enable profile image')
    ogp_app_id         = StringField('OGP app id')
    enable_twittercard = BooleanField('Enable twitter card')
    twitter_username   = StringField('Twitter username')
    display_poweredby =  BooleanField('Display powered by Logpot')
