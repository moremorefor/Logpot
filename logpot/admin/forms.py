#-*- coding: utf-8 -*-

from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileField
from wtforms import TextField
# from wtforms.validators import Required
from flask.ext.admin.contrib.sqla.fields import QuerySelectField
from flask.ext.login import current_user

from logpot.ext import db
from logpot.entry.models import Entry


class FileUploadForm(Form):
    uploadfile = FileField('image', validators=[FileRequired('Please select image')])
    name = TextField('Filename')
    entry_id = QuerySelectField(
        query_factory=lambda: db.session.query(Entry).filter_by(author=current_user).all()
    )

    # def validate(self):
    #     rv = Form.validate(self)
    #     if not rv:
    #         return False
