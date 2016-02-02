#-*- coding: utf-8 -*-

from logpot.admin.base import AuthenticateView, CommonModelView, checkFieldEmpty
from logpot.entry.models import Entry
from logpot.ext import db

from flask import flash, url_for
from flask.ext.login import current_user
from flask_admin.form import rules
# from logpot import rules
from flask.ext.admin.contrib.sqla.view import log
from flask.ext.admin.babel import gettext

from jinja2 import Markup

import misaka
import pygments
import os
import os.path as op


##===================================================================
##  Views
##===================================================================


class EntryModelView(AuthenticateView, CommonModelView):
    create_template = 'admin/entry/create.html'

    column_list = (
        'title',
        'slug',
        'category',
        'tags',
        'author',
        'is_published',
        'updated_at'
    )
    column_searchable_list = ("title", "summary", "slug")

    def _link_title(view, context, model, name):
        e = db.session.query(Entry).filter_by(id=model.id).one()

        return Markup('<a href="{0}" target="new">{1}</a>'.format(
            url_for('entry.entry', slug=e.slug), e.title
        ))

    column_formatters = {
        'title': _link_title
    }

    form_args = dict(
        title=dict(validators=[checkFieldEmpty]),
        slug=dict(validators=[checkFieldEmpty]),
        summary=dict(validators=[checkFieldEmpty]),
        md_body=dict(validators=[checkFieldEmpty]),
        category=dict(allow_blank=True)
    )

    def create_model(self, form):
        form.body.data = renderMarkdown(form.slug.data, form.md_body.data)
        form.author.data = current_user
        if super().create_model(form):
            return True

    def update_model(self, form, model):
        form.body.data = renderMarkdown(form.slug.data, form.md_body.data)
        # Update image direcotry
        if model.images:
            if not model.slug == form.slug.data:
                updateImageDirectory(model.slug, form.slug.data)
        if super().update_model(form, model):
            return True


class CategoryModelView(AuthenticateView, CommonModelView):
    column_list = (
        'name',
        'updated_at'
    )

    form_excluded_columns = ('entries', 'created_at', 'updated_at')

    form_rules = [
        rules.Field('name')
    ]

    form_args = dict(
        name=dict(validators=[checkFieldEmpty])
    )


class TagModelView(AuthenticateView, CommonModelView):
    column_list = (
        'name',
        'updated_at'
    )

    form_excluded_columns = ('entries', 'created_at', 'updated_at')

    form_rules = [
        rules.Field('name')
    ]

    form_args = dict(
        name=dict(validators=[checkFieldEmpty])
    )

##===================================================================
##  Utils
##===================================================================

class BleepRenderer(misaka.HtmlRenderer, misaka.SmartyPants):

    slug = ""

    def set_slug(self, slug):
        self.slug = slug

    def link(self, link, title, content):
        return '\n<a href="%(link)s" title="%(title)s" target="_blank">%(content)s</a>\n' % \
            {'link': link, 'content': content, 'title': title}

    def image(self, link, title, alt_text):
        return '\n<img src="/entry/%(slug)s/%(link)s" alt="%(alt_text)s" title="%(title)s"/>\n' % \
            {'link': link, 'title': title, 'alt_text': alt_text, 'slug': self.slug}

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(text, lexer, formatter)


def renderMarkdown(slug, body):
    renderer = BleepRenderer()
    renderer.set_slug(slug)
    misaka_md = misaka.Markdown(
        renderer,
        extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)
    misaka_content = misaka_md.render(body)
    return misaka_content


def updateImageDirectory(oldSlug, newSlug):
    oldPath = op.join(current_app.config['UPLOAD_DIRECTORY'], oldSlug)
    newPath = op.join(current_app.config['UPLOAD_DIRECTORY'], newSlug)
    os.rename(oldPath, newPath)
