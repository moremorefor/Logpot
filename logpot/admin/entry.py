#-*- coding: utf-8 -*-

from logpot.admin.base import AuthenticateView, CommonModelView, checkFieldEmpty

from flask import flash
from flask.ext.login import current_user
from flask.ext.admin.form import rules
# from logpot import rules
from flask.ext.admin.contrib.sqla.view import log
from flask.ext.admin.babel import gettext

import misaka
import pygments


##===================================================================
##  Views
##===================================================================


class EntryModelView(AuthenticateView, CommonModelView):
    create_template = 'admin/entry/create.jade'

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

    form_args = dict(
        title=dict(validators=[checkFieldEmpty]),
        slug=dict(validators=[checkFieldEmpty]),
        summary=dict(validators=[checkFieldEmpty]),
        md_body=dict(validators=[checkFieldEmpty]),
        category=dict(allow_blank=True)
    )

    form_create_rules = [
        rules.Header('Entry'),
        rules.Field('title'),
        rules.Field('slug'),
        rules.Field('category'),
        rules.Field('tags'),
        rules.Field('summary'),
        rules.HTML(
            """
            <div class="form-group clearfix">
            <label for="md_body" class="col-md-2 control-label">Body
                <strong style="color: red">*</strong>
            </label>
            <div class="preview_md">
                <textarea class="form-control" id="autosizable" name="md_body" v-model="input">
                </textarea>
            </div>


            <div class="preview">
                <div v-html="input | marked"></div>
            </div>
            </div>
            """
        ),
        rules.Field('is_published'),
        rules.Field('images')
    ]

    def create_model(self, form):
        form.body.data = renderMarkdown(form.slug.data, form.md_body.data)
        form.author.data = current_user
        if super().create_model(form):
            return True

    def update_model(self, form, model):
        form.body.data = renderMarkdown(form.slug.data, form.md_body.data)
        if super().update_model(form, model):
            return True


class CategoryModelView(AuthenticateView, CommonModelView):
    column_list = (
        'name',
        'updated_at'
    )

    form_create_rules = form_edit_rules = [
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

    form_create_rules = form_edit_rules = [
        rules.Field('name')
    ]

    form_args = dict(
        name=dict(validators=[checkFieldEmpty])
    )

##===================================================================
##  Utils
##===================================================================


class BleepRenderer(misaka.HtmlRenderer, misaka.SmartyPants):

    SLUG = ""

    @classmethod
    def setSlug(self, slug):
        self.SLUG = slug

    # def __init__(self, *args, **kwargs):
    #     self.dummy = args.pop("dummy")
    #     misaka.HtmlRenderer.__init__(self, *args, **kwargs)

    def link(self, link, title, content):
        return '\n<a href="%(link)s" target="_blank">%(content)s - %(title)s</a>\n' % \
            {'link': link, 'content': content, 'title': title}

    def image(self, link, title, alt_text):
        return '\n<img src="/entry/%(slug)s/%(link)s" alt="%(alt_text)s" title="%(title)s"/>\n' % \
            {'link': link, 'title': title, 'alt_text': alt_text, 'slug': self.SLUG}

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.HtmlFormatter()
        return pygments.highlight(text, lexer, formatter)


def renderMarkdown(slug, body):
    BleepRenderer.setSlug(slug)
    renderer = BleepRenderer()
    misaka_md = misaka.Markdown(
        renderer,
        extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)
    misaka_content = misaka_md.render(body)
    return misaka_content
