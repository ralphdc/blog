#!/usr/bin/env python3

from flask_script import  Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app import app
from app import db
from app.models import *


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='127.0.0.1',  port=5000))



@manager.option('-a', '--action', dest='action', default='')
@manager.option('-f', '--file', dest='fname', default='')
def blog_execute_command(action, fname):

    if not action:
        raise Exception("[Error] - action is empty!")

    from cli import BgCommand
    handler = BgCommand.get_unit(action, fname=fname)
    handler.run()


if __name__ == '__main__':
    manager.run()

