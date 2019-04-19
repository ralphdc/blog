#!/usr/bin/env python3


from .db import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager


class Visit(db.Model):

    __tablename__ = 'bg_visit'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    visit_name = db.Column(db.String(255), nullable=False)
    visit_ip = db.Column(db.String(255), nullable=True)

    created_at =  db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


class User(UserMixin, db.Model):

    __tablename__ = 'bg_user'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_name = db.Column(db.String(255), nullable=False, index=True, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    user_url = db.Column(db.String(255), nullable=True)
    user_status = db.Column(db.CHAR(1), nullable=False, server_default='0')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    #添加id属性， 解决flask_login读取id字段不兼容的问题；
    @property
    def id(self):
        return self.user_id

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.user_password = generate_password_hash(pwd)


    def check_password(self, pwd):
        return check_password_hash(self.user_password, pwd)

    def __init__(self, user_name, user_password, user_email, user_url):
        self.user_name = user_name
        self.password = user_password
        self.user_email = user_email
        self.user_url = user_url

class AnonymousUser(AnonymousUserMixin):
    '''
    继承至该类的用户模型 将作为未登陆时的用户模型,可以保持代码的一致性。
    '''
    def is_admin(self): # 自行定义的方法,用于权限判断
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))