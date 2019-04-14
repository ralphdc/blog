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



