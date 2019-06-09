#!/usr/bin/env python3

from flask import render_template, make_response, jsonify, request, flash, session
from app import app, db
from app.models import User
from sqlalchemy import func
from app.utils import *
from . import auth


@auth.route('/user', methods=['GET', 'POST'])
def auth_user():


    if request.method == 'POST':
        #页面容量；
        limit = request.form.get('limit') or app.config.get('PAGE_LIMIT')
        #页码；
        offset = request.form.get('offset') or app.config.get('PAGE_OFFSET')

        username = request.form.get('username')

        qy = db.session.query(User.user_name, User.user_email, User.user_url, User.user_status, User.created_at)
        if username:
            qy = qy.filter(User.user_name==username)

        count = db.session.query(func.count(User.id)).scalar()

        qy = qy.limit(limit).offset((offset-1) * limit)
        qy = qy.all()

        if qy:
            title = ('user_name', 'user_email', 'user_url', 'user_status', 'created_at')
            rows = make_row(title, qy)
            return make_response(jsonify({"code":0, "message":"SUCCESS", "rows": rows, "count":count}))

    else:

        if session.get('user').get('user_name') != 'administrator':
            flash('目前只有超级管理员才具有用户管理权限！')
        return render_template('auth/user/index.html')



