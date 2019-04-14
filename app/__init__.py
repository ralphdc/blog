#!/usr/bin/env python3

from flask import Flask
from config import Config
from .utils import check_login
from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config.from_object(Config())

db = SQLAlchemy(app)

login = LoginManager(app)

from .views import *









