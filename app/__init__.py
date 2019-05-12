#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from config import Config
from .utils import check_login
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
import redis
from .logger import handler

app = Flask(__name__)

app.config.from_object(Config())

db = SQLAlchemy(app)

csrf = CsrfProtect(app)
@csrf.error_handler
def csrf_error(reason):
    if request.is_xhr:
        return make_response(jsonify({"code": 1, "message":"[Error] csrf token error!"}))
    return render_template('csrf_error.html', reason=reason), 400


login_manager = LoginManager(app)
# 可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户。
login_manager.session_protection = 'strong'
# 这里填写你的登陆界面的路由
login_manager.login_view = 'app_login'


redisCache = redis.Redis(connection_pool=redis.ConnectionPool(
    host=app.config.get('REDIS_HOST'),
    port=app.config.get('REDIS_PORT'),
    db=app.config.get('REDIS_DB'))
)



from .views import *
from .main import main as main_blueprint
from .setting import setting as setting_blueprint
from .msgboard import msgboard as msgboard_blueprint
from .auth import auth as auth_blueprint

app.register_blueprint(main_blueprint, url_prefix='/main')
app.register_blueprint(setting_blueprint, url_prefix='/setting')
app.register_blueprint(msgboard_blueprint, url_prefix='/msgboard')
app.register_blueprint(auth_blueprint, url_prefix='/auth')


app.logger.addHandler(handler)
app.logger.info("------------------application init complete!-----------------")




