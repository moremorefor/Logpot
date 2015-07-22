#-*- coding: utf-8 -*-

from flask import current_app, flash, url_for, request
from flask.ext.admin import expose, BaseView

from logpot.admin.base import AuthenticateView, flash_errors
from logpot.admin.forms import SettingForm
from logpot.utils import loadSiteConfig, saveSiteConfig

import os
import mimetypes

class SettingView(AuthenticateView, BaseView):

    def getDirectoryPath(self):
        dirpath = os.path.join(current_app.config['UPLOAD_DIRECTORY'], 'settings')
        if os.path.exists(dirpath):
            return dirpath
        else:
            os.makedirs(dirpath)
            return dirpath

    def getFileExtention(self, mimetype):
        ext = mimetypes.guess_extension(mimetype)
        if ext == ".jpe":
            ext = ".jpg"
            return ext
        elif ext is None:
            ext = '.jpg'
            return ext
        else:
            return ext

    @expose('/', methods=('GET','POST'))
    def index(self):
        form = SettingForm()

        if form.validate_on_submit():
            if form.profile_img.data:
                file = form.profile_img.data
                ext = self.getFileExtention(file.mimetype)
                dirpath = self.getDirectoryPath()
                path = os.path.join(dirpath, "profile" + ext)
                file.save(path)

            data = {}
            data['site_title'] = form.title.data
            data['site_subtitle'] = form.subtitle.data
            data['site_author'] = form.author.data
            data['enable_link_github'] = form.enable_link_github.data
            data['enable_profile_img'] = form.enable_profile_img.data
            data['display_poweredby'] = form.display_poweredby.data
            if saveSiteConfig(current_app, data):
                flash('Successfully saved.')
            else:
                flash_errors('Oops. Save error.')
        else:
            flash_errors(form)

        data = loadSiteConfig(current_app)
        form.title.data               = data['site_title']
        form.subtitle.data            = data['site_subtitle']
        form.author.data              = data['site_author']
        form.enable_link_github.data  = data['enable_link_github']
        form.enable_profile_img.data  = data['enable_profile_img']
        form.display_poweredby.data   = data['display_poweredby']
        return self.render('admin/setting.html', form=form)
