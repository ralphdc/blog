#!/usr/bin/env python3

from flask_script import  Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.appsql import appdb


app = create_app()
manager = Manager(app)
appdb.init_app(app)
migrate = Migrate(app, appdb)


def make_shell_context():
    return dict(app=app, appdb=appdb)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='127.0.0.1',  port=5000))





if __name__ == '__main__':
    manager.run()

