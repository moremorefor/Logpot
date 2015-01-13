#-*- coding: utf-8 -*-

from logpot.auth.models import User
from logpot.entry.models import Entry, Category, Tag
from logpot.app import app
from logpot.ext import db
from logpot.admin.entry import renderMarkdown


def init_db():
    db.create_all()


def drop_db():
    db.drop_all()


def init_user():
    password = User.generate_password_hash(app.config["PASSWORD"])
    u = User(name=app.config["ADMIN"], email=app.config["EMAIL"], password=password)
    db.session.add(u)
    db.session.commit()
    db.session.remove()


def init_admin_user(name, email, password):
    password = User.generate_password_hash(password)
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    db.session.remove()


def init_category():
    c = Category(name='Python')
    c2 = Category(name='Objective-C')
    db.session.add(c)
    db.session.add(c2)
    db.session.commit()
    db.session.remove()


def init_tag():
    t = Tag(name='Flask')
    t2 = Tag(name='Django')
    db.session.add(t)
    db.session.add(t2)
    db.session.commit()
    db.session.remove()


def add_tag(name):
    t = Tag(name=name)
    db.session.add(t)
    db.session.commit()
    db.session.remove()


def init_entry():
    u = User.query.get(1)
    c = Category.query.get(1)
    t = Tag.query.get(1)
    s = 'entryslug'
    md_body = (
        "# This is H1 heading.\n" +
        "## This is H2 heading.\n" +
        "### This is H3 heading.\n" +
        "#### This is H4 heading.\n" +
        "\n" +
        "[Google](http://google.co.jp 'Title')\n" +
        "\n" +
        "```python\n" +
        "print('uuuu')\n" +
        "```\n"
    )

    body = renderMarkdown(s, md_body)

    entries01 = Entry(
        title=u'Title sample',
        summary=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        md_body=md_body,
        body=body,
        slug=s,
        category_id=c.id,
        user_id=u.id,)
    entries01.tags.append(t)
    db.session.add(entries01)
    db.session.commit()
    db.session.remove()


def show_entry():
    for entry in db.session.query(Entry).all():
        print (entry, entry.tags, entry.category, entry.author)
