#!/usr/bin/env python3


from .Default import Default

class Develop(Default):


    DEBUG = True

    #sqlalchemy
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

    REDIS_POOL_INSTANCE = 10

    REDIS_DB = 1

    REDIS_TIMEOUT = 20 * 60

    REDIS_AUTH_PREFIX = 'auth'

    BOARD_COMMENT_TIME_LIMIT = 5

    COOKIE_MAX_AGE = 7 * 24 * 60

    IMMUNITY_PATH = ['login', 'static']

    UPLOAD_FILE_PATH = "D:/github/blog/upload/"