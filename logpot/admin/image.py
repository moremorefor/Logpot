#-*- coding: utf-8 -*-

from logpot.ext import db
from logpot.entry.models import Entry
from logpot.image.models import Image
from logpot.admin.base import AuthenticateView, CommonModelView, flash_errors
from logpot.admin.forms import FileUploadForm
from logpot.utils import ImageUtil, getDirectoryPath

from flask import current_app, flash, url_for, request, redirect
from flask.ext.admin import expose

from werkzeug.utils import secure_filename
from jinja2 import Markup

import os
import mimetypes

class ImageModelView(AuthenticateView, CommonModelView):
    column_list = (
        'path',
        'name',
        'entry',
        'updated_at'
    )

    can_edit = False

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        e = db.session.query(Entry).filter_by(id=model.entry_id).one()
        name, ext = os.path.splitext(model.path)

        return Markup('<img src="{0}">'.format(
            url_for('img_upload_thumb_s', slug=e.slug, filename=name, ext=ext)
        ))

    column_formatters = {
        'path': _list_thumbnail
    }

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = FileUploadForm()

        if form.validate_on_submit():
            current_app.logger.info(request.files)  # MultiDict
            current_app.logger.info(request.files.getlist('uploadfile'))  # List
            current_app.logger.info(request.form)

            num = len(request.files.getlist('uploadfile'))

            for i in list(range(num)):
                # Check whether multiple files are selected
                file = request.files.getlist('uploadfile')[i]
                if file.filename == '':
                    # send error
                    form.uploadfile.errors.append('Please select image')
                    flash_errors(form)
                    return self.render(
                        'admin/upload.html',
                        form=form,
                        return_url=url_for('.index_view')
                    )

            for i in list(range(num)):
                file = request.files.getlist('uploadfile')[i]

                name = request.form.getlist('name')[i]
                if name != '':
                    name = secure_filename(name)
                else:
                    name = secure_filename(file.filename)
                    name = name.split('.')[0].strip()

                entry_id = request.form.getlist('entry_id')[i]
                e = db.session.query(Entry).filter_by(id=entry_id).one()

                ext = ImageUtil.getFileExtention(file.mimetype)
                dirpath = getDirectoryPath(current_app, e.slug)
                path = name + ext
                file.save(os.path.join(dirpath, path))

                current_app.logger.info(
                    'Name:  ' + name + '\n' +
                    'path:  ' + path + '\n' +
                    'Entry_id:  ' + entry_id)

                image = Image(
                    name=name,
                    path=path,
                    entry_id=entry_id
                )
                db.session.add(image)
                db.session.commit()

            flash('File Upload Success.')
            return redirect(url_for('.index_view'))
        else:
            flash_errors(form)
        return self.render('admin/upload.html', form=form, return_url=url_for('.index_view'))
