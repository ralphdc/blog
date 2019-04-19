#!/usr/bin/env python3

from flask import Flask
from config import Config
from .utils import check_login
from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_sqlalchemy import SQLAlchemy
import pymongo
import redis


app = Flask(__name__)

app.config.from_object(Config())

db = SQLAlchemy(app)

login_manager = LoginManager(app)
# 可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户。
login_manager.session_protection = 'strong'
# 这里填写你的登陆界面的路由
login_manager.login_view = 'app_login'

mongo = pymongo.MongoClient(app.config.get('MONGO_DATABASE_URI'))

redisCache = redis.Redis(connection_pool=redis.ConnectionPool(
    host=app.config.get('REDIS_HOST'),
    port=app.config.get('REDIS_PORT'),
    db=app.config.get('REDIS_DB'))
)

from .views import *









