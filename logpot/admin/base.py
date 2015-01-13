#-*- coding: utf-8 -*-

from flask.ext.admin import expose, AdminIndexView, BaseView
from flask.ext.admin.contrib.sqla import ModelView

from flask import flash, current_app
from flask.ext.login import login_required, current_user


def flash_errors(form):
    """Flashes form errors"""
    current_app.logger.info(form.errors)
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                field,
                error
            ), 'error')


def checkFieldEmpty(form, field):
    # send error
    if field.data == '':
        current_app.logger.info(field)
        flash(u"Error in the %s field - %s" % (
            field.name,
            'Please input'
        ), 'error')


class AuthenticateView(object):

    def is_accessible(self):
        return current_user.is_authenticated()


class CommonModelView(ModelView):
    form_excluded_columns = ('created_at', 'updated_at')

    def after_model_change(self, form, model, is_created):
        flash('Success.')

    def on_model_delete(self, model):
        flash('Delete Success.')


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.jade')


class MyView(AuthenticateView, BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/test.jade')

    @expose('/test/')
    def test(self):
        return self.render('admin/test.jade')
