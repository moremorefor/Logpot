#-*- coding: utf-8 -*-

from flask.ext.script import Manager, prompt, prompt_bool, prompt_pass
from db_create import (
    init_db,
    drop_db,
    init_user,
    init_admin_user,
    init_entry,
    init_category,
    init_tag,
    add_tag,
    show_entry
)
from flask.ext.migrate import MigrateCommand
from logpot.app import app


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(debug=True, threaded=True)


@manager.command
def init_admin():
    name = prompt('Resister admin user.\n[?] input username: ')
    email = prompt('[?] input email: ')
    password = prompt_pass('[?] input password: ')
    confirm_password = prompt_pass('[?] input password again: ')

    if not password == confirm_password:
        print('Password does not match.')
        return False
    else:
        init_admin_user(name, email, password)
        return True


@manager.command
def initall():
    if prompt_bool("Are you sure you want to create DB and initialize?"):
        drop_db()
        init_db()
        if init_admin():
            init_category()
            init_tag()
            init_entry()


@manager.command
def initdb():
    if prompt_bool("Are you sure you want to create DB"):
        init_db()


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        drop_db()


@manager.command
def inituser():
    if prompt_bool("Are you sure you want to create sample user"):
        init_user()


@manager.option('-n', '--name', help='Tag name')
def addtag(name):
    if prompt_bool("Add this Tag: %r ?" % name):
        add_tag(name)


@manager.command
def initentry():
    if prompt_bool('Are you sure you want to create sample entry'):
        init_entry()


@manager.command
def showentry():
    show_entry()


if __name__ == "__main__":
    manager.run()
