#-*- coding: utf-8 -*-

from flask.ext.admin.form import rules

from logpot.auth.models import User
from logpot.admin.base import AuthenticateView, CommonModelView


class UserModelView(AuthenticateView, CommonModelView):
    column_list = (
        'name',
        'email',
        'password',
        'updated_at'
    )

    def _list_password(view, context, model, name):
        return model.password.split('$')[1]

    column_formatters = {
        'password': _list_password
    }

    column_searchable_list = (User.name, User.email)


    form_create_rules = [
        rules.Field('name'),
        rules.Field('email'),
        rules.Field('password')
    ]

    form_edit_rules = [
        rules.Field('name'),
        rules.Field('email'),
        rules.Field('password')
    ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self.form_widget_args = dict(
            password = dict()
        )
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self.form_widget_args = dict(
            password = dict(readonly=True)
        )
        return form

    def create_model(self, form):
        form.password.data = User.generate_password_hash(str(form.password))
        if super().create_model(form):
            return True

    def update_model(self, form, model):
        form.password.data = model.password
        if super().update_model(form, model):
            return True