#!/usr/bin/env python3

#存放装饰器；

from functools import wraps
from flask import request, redirect, render_template, session, url_for
import os
import hashlib


def check_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('loginTag'):
            return redirect(url_for('app_login'))
        return func(*args, **kwargs)
    return decorated_function





def getRandomKey():

    return hashlib.md5(os.urandom(24)).hexdigest()