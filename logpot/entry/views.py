#-*- coding: utf-8 -*-

from logpot.entry.models import Entry
from logpot.entry import bp

from logpot.ext import db

from flask import redirect, current_app
from flask import render_template, url_for
from flask.ext.sqlalchemy import Pagination

import calendar

##===================================================================
##  Utils
##===================================================================


def ord(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def formatDatetime(datetime):
    result_date = datetime.strftime('%Y-%m-%d')
    return result_date


##===================================================================
##  Routing
##===================================================================


@bp.route('/')
@bp.route('/<int:page>', methods=['GET'])
def entries(page=1):
    p = Entry.query.outerjoin(Entry.category).order_by(Entry.id.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    entries = p.items
    if len(entries) == 0:
        print('There are no entries.')
        abort(404)
    else:
        for e in entries:
            e.updated = formatDatetime(e.updated_at)
    return render_template('entry/entries.html', title='Home', entries=entries, pagination=p)


@bp.route('/<slug>')
def entry(slug):
    entry = db.session.query(Entry).filter_by(slug=slug).outerjoin(Entry.category).one()
    if not entry:
        print('No such entry.')
        # abort(404)
    else:
        entry.updated = formatDatetime(entry.updated_at)
        return render_template('entry/entry.html', entry=entry, this_url=url_for('.entry', slug=slug))
