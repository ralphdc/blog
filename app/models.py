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


    def __init__(self, visit_name, visit_ip):
        self.visit_name = visit_name
        self.visit_ip = visit_ip


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

    def get_user_role(self):
        return db.session.query()


    def __init__(self, user_name, user_password, user_email, user_url):
        self.user_name = user_name
        self.password = user_password
        self.user_email = user_email
        self.user_url = user_url

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class AnonymousUser(AnonymousUserMixin):
    '''
    继承至该类的用户模型 将作为未登陆时的用户模型,可以保持代码的一致性。
    '''
    def is_admin(self): # 自行定义的方法,用于权限判断
        return False
login_manager.anonymous_user = AnonymousUser


class BoardUser(db.Model):

    __tablename__ = 'bg_board_user'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    board_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    board_user_nickname = db.Column(db.String(255), nullable=False)
    board_user_email = db.Column(db.String(255), nullable=False)
    board_user_url = db.Column(db.String(255), nullable=True)
    board_user_ip = db.Column(db.String(255), nullable=True)
    board_user_status = db.Column(db.CHAR(1), nullable=False, server_default='1')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, nickname, email, url=None, ip=None, status='1'):

        self.board_user_nickname = nickname
        self.board_user_email = email
        self.board_user_url = url
        self.board_user_ip = ip
        self.board_user_status = status

class BoardContent(db.Model):

    __tablename__ = 'bg_board_content'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    board_content_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    board_content_uid = db.Column(db.Integer, nullable=False)
    board_content_body = db.Column(db.Text, nullable=False)
    board_content_type = db.Column(db.CHAR(1), nullable=False, server_default='1')
    board_content_target = db.Column(db.Integer, nullable=True)
    board_content_status = db.Column(db.CHAR(1), nullable=False, server_default='1')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, uid, body, type, target=None, status='1'):

        self.board_content_uid      = uid
        self.board_content_body     = body
        self.board_content_type     = type
        self.board_content_target   = target
        self.board_content_status   = status

class Role(db.Model):

    __tablename__ = 'bg_role'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    role_id     =  db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    role_name   = db.Column(db.String(255), nullable=False)
    role_des    = db.Column(db.String(255), nullable=True)
    role_status = db.Column(db.CHAR(1), nullable=False, server_default='1')
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, role_name, role_des='-', role_status='1'):

        self.role_name = role_name
        self.role_des = role_des
        self.role_status = role_status


class UserAndRole(db.Model):

    __tablename__ = 'bg_user_role_map'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }


    map_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    map_uid = db.Column(db.Integer, nullable=False)
    map_oid = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

class Module(db.Model):
    __tablename__ = 'bg_module'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    module_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    module_name     = db.Column(db.String(255), nullable=False)
    module_url      = db.Column(db.String(255), nullable=False)
    module_parent   = db.Column(db.Integer, nullable=False)
    module_status   = db.Column(db.CHAR(1), nullable=False, server_default='1')
    module_icon     = db.Column(db.String(255), nullable=False, server_default='fa fa-user')
    module_description = db.Column(db.String(255), nullable=True, server_default='-')
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, module_name, module_url, module_parent, module_status='1', module_icon='fa fa-user', module_description=None):
        self.module_name = module_name
        self.module_url = module_url
        self.module_parent = module_parent
        self.module_status = module_status
        self.module_icon = module_icon
        self.module_description = module_description



class RoleAndModule(db.Model):
    __tablename__ = 'bg_role_module_map'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    map_id      = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    role_id     =  db.Column(db.Integer, nullable=False)
    module_id   = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, role_id, module_id):
        self.role_id = role_id
        self.module_id = module_id



