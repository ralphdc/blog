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

    def get_user_name(self):
        return self.user_name

    def get_user_email(self):
        return self.user_email

    def get_user_id(self):
        return self.user_id

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
    board_content_status = db.Column(db.CHAR(1), nullable=False, server_default='0')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, uid, body, type, target=None, status='0'):

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


'''
class Article(db.Model):
    __tablename__ = 'bg_article'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }


    article_id  = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    article_title = db.Column(db.String(255), nullable=True, server_default='-') #标题；
    article_description = db.Column(db.String(1024), nullable=True, server_default='-') #内容摘要；
    article_content = db.Column(db.Text(), nullable=False, server_default='-') #文章内容
    article_creator = db.Column(db.String(255), nullable=True, server_default='-') #作者
    article_display = db.Column(db.CHAR(1), nullable=False, server_default='1') #是否显示
    article_limited = db.Column(db.CHAR(1), nullable=False, server_default='0')  #访问是否需密码；
    article_password = db.Column(db.String(255), nullable=True)
    article_top = db.Column(db.CHAR(1), nullable=True, server_default='0') #是否置顶
    article_status = db.Column(db.CHAR(1), nullable=True, server_default='0') # 发布/草稿
    article_allow = db.Column(db.CHAR(1), nullable=True, server_default='1') #是否允许评论

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())





    def __init__(self, **kwargs):
        self.article_title = kwargs.get('airticle_title')
        self.article_description = kwargs.get('article_description') or '-'
        self.article_content = kwargs.get('article_content')
        self.article_creator = kwargs.get('article_creator')
        self.article_display = kwargs.get('article_display') or '1'
        self.article_limited = kwargs.get('article_limited') or '0'
        self.article_top = kwargs.get('article_top') or '0'
        self.article_status = kwargs.geT('article_status') or '0'
        self.article_allow = kwargs.geT('article_allow') or '1'



        if not self.article_title or not self.article_content or not self.article_creator:
            raise Exception("[Error] - please check article's title or content or creator!")

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.article_password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.article_password, pwd)


class ArticleCategoryMap(db.Model):
    __tablename__ = 'bg_article_category_map'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    map_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    article_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())
    
    
    def __init__(self, **kwargs):
        self.article_id = kwargs.get('article_id')
        self.category_id = kwargs.get('category_id')
        
'''


class Category(db.Model):
    __tablename__ = 'bg_category'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    category_id  = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    category_content = db.Column(db.String(255), nullable=False)
    category_description = db.Column(db.String(1024), nullable=True)
    category_creator = db.Column(db.String(255), nullable=False)
    category_status = db.Column(db.CHAR(1), nullable=True, server_default='1')

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        self.category_content = kwargs.get('category_content')
        self.category_description = kwargs.get('category_description')
        self.category_creator = kwargs.get('category_creator')
        self.category_status = kwargs.get('category_status') or '1'

        if not self.category_content or not self.category_creator:
            raise Exception("[Error]- Please check category_content and category_creator!")





class Posts(db.Model):
    __tablename__ = 'bg_posts'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    posts_title = db.Column(db.String(255), nullable=False)
    posts_desc = db.Column(db.String(2048), nullable=False)
    posts_content = db.Column(db.Text, nullable=False)
    posts_status = db.Column(db.CHAR(1), nullable=False, server_default='1')
    posts_password = db.Column(db.String(255), nullable=True)
    posts_top = db.Column(db.CHAR(1), nullable=False, server_default='1')
    posts_allow = db.Column(db.CHAR(1), nullable=False, server_default='1')
    posts_creator = db.Column(db.String(255), nullable=False)
    posts_comment = db.Column(db.Integer, nullable=True)
    posts_visit = db.Column(db.Integer, nullable=True)
    posts_category = db.Column(db.String(1024), nullable=True)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.posts_password = generate_password_hash(pwd)

    def set_password(self, password):
        self.posts_password = generate_password_hash(password)

    def check_password(self, pwd):
        return check_password_hash(self.posts_password, pwd)


    def __init__(self, **kwargs):
        self.posts_title = kwargs.get('posts_title')
        self.posts_desc = kwargs.get('posts_desc')
        self.posts_content = kwargs.get('posts_content')
        self.posts_status = kwargs.get('posts_status')
        self.posts_top = kwargs.get('posts_top')
        self.posts_allow = kwargs.get('posts_allow')
        self.posts_creator = kwargs.get('posts_creator')
        self.posts_comment = kwargs.get('posts_comment') or 1
        self.posts_visit = kwargs.get('posts_visit') or 1
        self.posts_category = kwargs.get('posts_category')


class Album(db.Model):

    __tablename__ = 'bg_album'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    album_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, unique=True)
    album_name = db.Column(db.String(255), nullable=False)
    album_status = db.Column(db.CHAR(1), nullable=False, server_default='1')
    album_desc = db.Column(db.String(1024), nullable=True)
    album_creator = db.Column(db.String(255), nullable=True)
    album_slt = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, **kwargs):
        self.album_name = kwargs.get('album_name')
        self.album_status= kwargs.get('album_status') or '1'
        self.desc = kwargs.get('album_desc')
        self.album_creator = kwargs.get('creator') or 'admin'
        self.album_slt = kwargs.get('album_slt') or ''


class Photo(db.Model):
    __tablename__ = 'bg_photo'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    photo_name = db.Column(db.String(255), nullable=False)
    photo_upload_name = db.Column(db.String(255), nullable=False)
    phone_space = db.Column(db.String(255), nullable=True)
    photo_path = db.Column(db.String(255), nullable=False)
    photo_creator = db.Column(db.String(255), nullable=False)
    photo_status =  db.Column(db.CHAR(1), nullable=False, server_default='1')
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())


    def __init__(self, **kwargs):
        self.photo_name = kwargs.get('photo_name')
        self.photo_path = kwargs.get('photo_path')
        self.photo_upload_name = kwargs.get('photo_upload_name')
        self.phone_space = kwargs.get('photo_space')
        self.photo_creator = kwargs.get('photo_creator')
        self.photo_status = kwargs.get('photo_status') or '1'



class AlbumPhotoMap(db.Model):
    __tablename__ = 'bg_photomap'

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    map_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    album_id = db.Column(db.Integer, nullable=False)
    photo_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        self.album_id = kwargs.get('album_id')
        self.photo_id = kwargs.get('photo_id')