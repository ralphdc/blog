#!/usr/bin/env python3

from .Default import Default
import pymysql

class Product(Default):

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://blog:Blog1234@127.0.0.1:3306/blog?charset=utf8"

    SQLALCHEMY_POOL_SIZE = 5000

    SQLALCHEMY_POOL_TIMEOUT = 10

    SQLALCHEMY_POOL_RECYCLE = 1200

    SQLALCHEMY_MAX_OVERFLOW = 2000

    MONGO_DATABASE_URI = "mongodb://blog:Blog1234@127.0.0.1:27017/"

    MONGO_HOST = '127.0.0.1'

    MONGO_PORT = 27017

    MONGO_USER = 'blog'

    MONGO_PWD = 'Blog1234'

    MONGO_DB = 'blog'

    REDIS_HOST = '127.0.0.1'

    REDIS_PORT = 6379

    REDIS_DB = 1

    BOARD_COMMENT_TIME_LIMIT = 3

    UPLOAD_FILE_PATH = ""

    LOCAL_FILE_PATH = 'D:/github/blog/download'

    MYSQL_HOST = '127.0.0.1'

    MYSQL_PORT = 3306

    MYSQL_USER = 'blog'

    MYSQL_PWD = 'Blog1234'

    MYSQL_DB = 'blog'

    MYSQL_CHARSET = 'utf8'

    MYSQL_CURSOR = pymysql.cursors.DictCursor


