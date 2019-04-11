#!/usr/bin/env python3

from flask import Flask, render_template
from config import Config


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config())

    @app.route('/')
    def app_index():
        return 'Hello World!'

    @app.route('/admin')
    def app_admin():
        return render_template('admin.html')



    return app