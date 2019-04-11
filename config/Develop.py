#!/usr/bin/env python3


class Develop():

    BLOG_NAME = '天涯飞鸿'

    DEBUG = True

    #sqlalchemy
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://blog:Blog1234@47.100.56.218:3306/blog?charset=utf8"

    SQLALCHEMY_POOL_SIZE = 5000

    SQLALCHEMY_POOL_TIMEOUT = 10

    SQLALCHEMY_POOL_RECYCLE = 1200

    SQLALCHEMY_MAX_OVERFLOW = 2000



