#-*- coding: utf-8 -*-

from flask import current_app, flash, url_for, request
from flask.ext.admin import expose, BaseView

from logpot.admin.base import AuthenticateView, flash_errors
from logpot.admin.forms import SettingForm
from logpot.utils import ImageUtil, getDirectoryPath, loadSiteConfig, saveSiteConfig

import os
from PIL import Image

class SettingView(AuthenticateView, BaseView):

    def saveProfileImage(self, filestorage):
        buffer = filestorage.stream
        buffer.seek(0)
        image = Image.open(buffer)
        image = ImageUtil.crop_image(image, 64)
        current_app.logger.info(image)
        dirpath = getDirectoryPath(current_app, '_settings')
        filepath = os.path.join(dirpath, "profile.png")
        image.save(filepath, optimize=True)

    @expose('/', methods=('GET','POST'))
    def index(self):
        form = SettingForm()

        if form.validate_on_submit():
            if form.profile_img.data:
                file = form.profile_img.data
                self.saveProfileImage(file)

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
