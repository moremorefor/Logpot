#-*- coding: utf-8 -*-

from flask_admin import expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView

from flask import flash, current_app, redirect, url_for
from flask_login import login_required, current_user


def flash_errors(form):
    """Flashes form errors"""
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

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class CommonModelView(ModelView):
    form_excluded_columns = ('created_at', 'updated_at')

    # def after_model_change(self, form, model, is_created):
    #     flash('Success.')

    # def on_model_delete(self, model):
    #     flash('Delete Success.')


class IndexView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.html')
