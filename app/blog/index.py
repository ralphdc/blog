#!/usr/bin/env python3

from app import app, db
from flask import session, render_template, redirect, url_for, request, flash, make_response, jsonify
from sqlalchemy import and_
from app.models import Posts, Category
from app.utils import *
from app.Pagination import Pagination

@app.route('/')
def app_index():
    page_index = request.args.get('page') or '1'
    page_size = app.config.get('BLOG_PAGE_SIZE') or 5

    try:
        page_index = abs(int(page_index))
    except Exception:
        page_index = 1

    if page_index < 1:
        page_index = 1

    offset = (int(page_index) - 1) * page_size
    limit = int(page_size)

    qy = db.session.query(
        Posts.posts_id,
        Posts.posts_title,
        Posts.posts_desc,
        Posts.created_at,
        Category.category_image,
        Category.category_content
    ).outerjoin(Category, Category.category_id==Posts.posts_category)

    count = qy.count()
    qy = qy.limit(limit).offset(offset)
    qy = qy.all()

    pager_obj = Pagination(page_index, count, request.path, request.args, per_page_count=page_size)
    html = pager_obj.page_html()


    return render_template('index.html',  html = html, qy=qy)

@app.route('/article/<int:aid>', methods=['GET'])
def app_article(aid):
    if not aid:
        return render_template('404.html')

    qy = db.session.query(
        Posts.posts_title,
        Posts.posts_category,
        Posts.posts_allow,
        Posts.posts_content,
        Posts.created_at,
        Posts.posts_desc,
        Posts.posts_visit,
        Posts.posts_comment,
        Category.category_content,
        Posts.posts_password,
        Category.category_id,
        Posts.posts_tag,
        Posts.posts_allow
    )\
        .outerjoin(Category, Category.category_id==Posts.posts_category)\
        .filter(and_(Posts.posts_id==aid, Posts.posts_status=='1', Category.category_status=='1'))\
        .first()
    if not qy or not qy[0]:
        return render_template('404.html')
    if qy[11]:
        tags = qy[11].split('|')
    else:
        tags = None
    recommend = db.session.query(
        Posts.posts_id,
        Posts.posts_title
    )\
    .filter(and_(Posts.posts_category==qy[10], Posts.posts_id!=aid))\
    .order_by(Posts.created_at.desc()) \
    .limit(10)\
    .all()
    print(qy[12])
    return render_template('content.html', content=qy, pageClass="single", tags=tags, recommend=recommend)


@app.route('/comment', methods=['POST'])
def app_comment():
    post_id = request.form.get('post_id')
    nickname = request.form.get('nickname')
    site = request.form.get('site')
    body = request.form.get('comment_body')
    ip = request.remote_addr

    if not post_id or not nickname or not site or not body:
        return make_response(jsonify({"code": 1, "message":"数据提交不完整，请检查！"}))








