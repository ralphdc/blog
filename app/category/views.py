#!/usr/bin/env python3

from flask import render_template, make_response, jsonify, request, session

from app.utils import *
from app import db, app
from app.models import Category, User
from sqlalchemy import func
from . import category


@category.route('/', methods=['GET', 'POST'])
def category_index():

    if request.method == 'POST':

        category_name = request.form.get('category_name')

        # 页面容量；
        limit = request.form.get('limit') or app.config.get('PAGE_LIMIT')
        # 页码；
        offset = request.form.get('offset') or app.config.get('PAGE_OFFSET')

        limit = int(limit)
        offset = int(offset)

        qy = db.session.query(Category.category_id,Category.category_content, Category.category_creator, Category.category_status, Category.created_at, User.user_name) \
            .outerjoin(User, User.user_id==Category.category_creator)
        if category_name:
            qy = qy.filter(Category.user_name == category_name)
        count = db.session.query(func.count(Category.category_id)).scalar()
        qy = qy.limit(limit).offset((offset - 1) * limit)
        qy = qy.all()

        if qy:
            title = ('category_id','category_content', 'category_creator', 'category_status', 'created_at', 'user_name')
            rows = make_row(title, qy)
            return make_response(jsonify({"code": 0, "message": "SUCCESS", "rows": rows, "total": count}))
        else:
            return make_response(jsonify({"code": 1, "message": "查询数据库失败！"}))
    else:
        return render_template('category/index.html')



@category.route('/add', methods=['POST'])
@category.route('/add/<int:id>', methods=['POST'])
def category_add(id=None):

    category_content = request.form.get('category_content')
    category_status = request.form.get('category_status') or '1'
    category_description = request.form.get('category_description')

    if not category_content or not category_status:
        return make_response(jsonify({"code":1, "message": "请填写分类标题！"}))

    if id:
        pass
    else:
        try:
            category = Category(category_content=category_content, category_description=category_description, category_creator=current_user.user_name, category_status=category_status)
            db.session.add(category)
            db.session.commit()
            return make_response(jsonify({"code": 0, "message": "提交成功"}))
        except Exception as e:
            app.logger.exception(e)
            return make_response(jsonify({"code": 1, "message": "执行错误，请联系管理员！"}))





