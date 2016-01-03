#-*- coding: utf-8 -*-

import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from flask.ext.script import Manager, prompt, prompt_bool, prompt_pass
from db_create import (
    init_db,
    drop_all,
    init_admin_user,
    init_entry,
    init_category,
    init_tag
)
from flask.ext.migrate import MigrateCommand
from logpot.app import app

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(threaded=True)


@manager.command
def initialize():
    if prompt_bool("Are you sure you want to initialize all ?"):
        admin = init_admin()
        if admin:
            drop_all(app)
            init_db()
            init_admin_user(admin["name"], admin["email"], admin["password"])
            init_category()
            init_tag()
            init_entry()
            print('Success!')

@manager.command
def init_admin():
    name = prompt('Resister admin user.\n[?] input username: ')
    email = prompt('[?] input email: ')
    password = prompt_pass('[?] input password: ')
    confirm_password = prompt_pass('[?] input password again: ')

    if password != confirm_password:
        print('Password does not match.')
        return False
    else:
        return {"name":name, "email":email, "password":password}


if __name__ == "__main__":
    manager.run()
