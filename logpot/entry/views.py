#-*- coding: utf-8 -*-

from logpot.entry.models import Entry
from logpot.entry import bp

from logpot.ext import db

from flask import redirect, current_app
from flask import render_template, url_for

import calendar

##===================================================================
##  Utils
##===================================================================


def ord(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def formatDatetime(datetime):
    year = datetime.year
    month = calendar.month_abbr[datetime.month]
    day = ord(datetime.day)
    result_date = '{m} {d} {y}'.format(y=year, m=month, d=day)
    return result_date


##===================================================================
##  Routing
##===================================================================


@bp.route('/')
@bp.route('/<int:page>', methods=['GET'])
def entries(page=1):
    entries = Entry.query.outerjoin(Entry.category).paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
    if len(entries) == 0:
        return redirect(url_for('entry.entries'))
    else:
        for e in entries:
            e.updated_at = formatDatetime(e.updated_at)
    # logging.info(request.headers.get('User-Agent'))
    return render_template('entry/entries.jade', title='Home', entries=entries)


@bp.route('/<slug>')
def entry(slug):
    entry = db.session.query(Entry).filter_by(slug=slug).outerjoin(Entry.category).one()
    if not entry:
        print('No such entry.')
        # abort(404)
    else:
        entry.updated_at = formatDatetime(entry.updated_at)
        return render_template('entry/entry.jade', entry=entry, this_url=url_for('.entry', slug=slug))
