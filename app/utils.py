#!/usr/bin/env python3

#存放装饰器；

from functools import wraps
from flask import request, redirect, render_template, session, url_for
import os
import hashlib
from app import rdx
from app import app
import pymysql

def check_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('loginTag'):
            return redirect(url_for('app_login'))
        return func(*args, **kwargs)
    return decorated_function


def getRandomKey():

    return hashlib.md5(os.urandom(24)).hexdigest()

def get_ukey():
    return session['ukey'] or redis_get('ukey')

def get_user_key(user_name):
    return "{}:{}".format(app.config.get('REDIS_AUTH_PREFIX'), user_name)

def make_row(title, datas):

    if not isinstance(datas, list):
        raise Exception("[Error] - datas error! It must to be list!")

    if not isinstance(title, tuple):
        raise Exception("[Error] - title type error! It must to be tuple!")

    if len(title) != len(datas[0]):
        raise Exception("[Error] - row data not match!")

    row = []
    for data in datas:
        row.append(dict(zip(title, data)))

    return row


def redis_get(key):
    return rdx.get(key)

def redis_set(key, value, timeout=None):
    rdx.set(key, value, ex=timeout if timeout else app.config.get('REDIS_TIMEOUT'))


def get_mysql_config():

    return {
        'host': app.config.get('MYSQL_HOST'),
        'port':  app.config.get('MYSQL_PORT'),
        'user':  app.config.get('MYSQL_USER'),
        'password':  app.config.get('MYSQL_PWD'),
        'db':  app.config.get('MYSQL_DB'),
        'charset':  app.config.get('MYSQL_CHARSET'),
        'cursorclass': app.config.get('MYSQL_CURSOR')
    }

def mysql_fetch_one(sql, kvs=None):
    connection = pymysql.connect(**get_mysql_config())
    _rtf = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, kvs)
            _rtf = cursor.fetchone()
    except Exception:
        raise
    finally:
        connection.close()
    return _rtf

def mysql_fetch_all(sql, kvs=None):
    connection = pymysql.connect(**get_mysql_config())
    _rtf = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, kvs)
            _rtf = cursor.fetchall()
    except Exception:
        raise
    finally:
        connection.close()
    return _rtf



def mysql_execute(sql, kvs):
    connection = pymysql.connect(**get_mysql_config())
    _rtf = 0
    try:
        with connection.cursor() as cursor:
            _rtf = cursor.execute(sql,kvs)
        # 默认不自动提交事务，所以需要手动提交
        connection.commit()
    except Exception :
        raise
    finally:
        connection.close()

    return _rtf
