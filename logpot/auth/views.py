#-*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required

from logpot.auth import bp
from logpot.auth.forms import LoginForm
from logpot.auth.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated():
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if not user:
            flash('User or Password is not correct.')
            return render_template('auth/login.html', title='Login', form=form)
        login_user(user)
        flash('Logged in successfully.')
        current_app.logger.info('login success.')
        current_app.logger.info('User: %r' % user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout success.")
    return redirect(url_for('index'))
