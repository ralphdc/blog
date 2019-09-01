#!/usr/bin/env python3

from app import app, db
from flask import session, render_template, redirect, url_for, request, flash, make_response, jsonify
from sqlalchemy import and_
from app.models import Posts, Category, Comments
from app.utils import *
from app.Pagination import Pagination
import datetime
import time

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

    recommend = db.session.query(
        Posts.posts_id,
        Posts.posts_title,
        Posts.posts_desc,
        Posts.created_at,
        Posts.posts_seo,
        Category.category_image,
        Category.category_content,
    ).outerjoin(Category, Category.category_id==Posts.posts_category)\
    .filter(and_(Posts.posts_status=='1', Category.category_status=='1', Posts.posts_top=='1'))\
    .order_by(Posts.created_at.desc())\
    .first()

    qy = db.session.query(
        Posts.posts_id,
        Posts.posts_title,
        Posts.posts_desc,
        Posts.created_at,
        Posts.posts_seo,
        Category.category_image,
        Category.category_content,
    )\
    .outerjoin(Category, Category.category_id == Posts.posts_category)\
    .filter(and_(Posts.posts_status=='1', Category.category_status=='1'))
    if recommend:
        qy = qy.filter(Posts.posts_id != recommend[0])
    qy = qy.order_by(Posts.created_at.desc())
    count = qy.count()
    qy = qy.limit(limit).offset(offset)
    qy = qy.all()


    pager_obj = Pagination(page_index, count, request.path, request.args, per_page_count=page_size)
    html = pager_obj.page_html()

    return render_template('index.html',  html = html, qy=qy, recommend=recommend)

@app.route('/article/<int:aid>', methods=['GET', 'POST'])
def app_article_aid(aid):
    if not aid:
        return render_template('404.html')

    check_pwd = request.form.get('readpwd') or None

    qy = db.session.query(
        Posts.posts_id,
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
    if qy[12]:
        tags = qy[12].split('|')
    else:
        tags = None

    if check_pwd:
        check_pwd_result = qy.check_password(check_pwd)
        print(check_pwd_result)

    #文章推荐
    recommend = db.session.query(
        Posts.posts_id,
        Posts.posts_title,
        Posts.posts_seo
    )\
    .filter(and_(Posts.posts_category==qy[10], Posts.posts_id!=aid))\
    .order_by(Posts.created_at.desc()) \
    .limit(10)\
    .all()

    #评论列表
    comments = db.session.query(
        Comments.comment_nickname,
        Comments.comment_body,
        Comments.created_at
    )\
    .filter(and_(Comments.comment_post_id==aid, Comments.comment_status=='1')) \
    .all()

    return render_template('content.html',
                           content=qy,
                           pageClass="single",
                           tags=tags,
                           recommend=recommend,
                           comments=comments,
                           check_pwd_path='/article/{}'.format(aid)
                           )

@app.route('/article/<string:seoTag>', methods=['GET', 'POST'])
def app_article_seoTag(seoTag):
    if not seoTag:
        return render_template('404.html')

    qy = db.session.query(
        Posts.posts_id,
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
        .filter(and_(Posts.posts_seo==seoTag, Posts.posts_status=='1', Category.category_status=='1'))\
        .first()
    if not qy or not qy[0]:
        return render_template('404.html')
    if qy[12]:
        tags = qy[12].split('|')
    else:
        tags = None

    #推荐
    recommend = db.session.query(
        Posts.posts_id,
        Posts.posts_title,
        Posts.posts_seo
    )\
    .filter(and_(Posts.posts_category==qy[11], Posts.posts_id!=qy[0]))\
    .order_by(Posts.created_at.desc()) \
    .limit(10)\
    .all()

    # 评论列表
    comments = db.session.query(
        Comments.comment_nickname,
        Comments.comment_body,
        Comments.created_at
    ) \
        .filter(and_(Comments.comment_post_id == qy[0], Comments.comment_status == '1')) \
        .all()
    return render_template('content.html',
                           content=qy,
                           pageClass="single",
                           tags=tags,
                           recommend=recommend,
                           comments=comments,
                           check_pwd_path='/article/{}'.format(seoTag)
                           )


@app.route('/comment', methods=['POST'])
def app_comment():
    post_id = request.form.get('post_id')
    nickname = request.form.get('nickname')
    site = request.form.get('site')
    body = request.form.get('comment_body')
    ip = request.remote_addr

    if not post_id or not nickname or not site or not body:
        return make_response(jsonify({"code": 1, "message":"数据提交不完整，请检查！"}))

    post_id = int(post_id)
    find_post_sql = "SELECT posts_title FROM bg_posts WHERE `posts_id`= %s"
    find_query = mysql_fetch_one(find_post_sql, (post_id))
    if not find_query or not find_query.get('posts_title'):
        return make_response(jsonify({"code": 1, "message":"您评论的文章不存在！"}))

    check_illegal = "SELECT `item_content` FROM `cli_illegal_items`"
    query = mysql_fetch_all(check_illegal)
    if query and len(query) > 0:
        for q in query:
            if q.get('item_content') in body or q.get('item_content') in nickname or q.get('item_content') in site:
                return make_response(jsonify({"code": 1,  "message":"您提交的信息包含敏感词汇，服务端拒绝接收！<br/>敏感词汇是：{}".format(q.get('item_content'))}))

    #每个IP地址，一天内只允许提交5条信息；
    current_date = datetime.datetime.now()
    yesterday_date = current_date - datetime.timedelta(hours=23, minutes=59, seconds=59)
    yesterday_date_string = yesterday_date.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(yesterday_date_string, "%Y-%m-%d %H:%M:%S")
    yesterday_timestamp = int(time.mktime(timeArray))


    check_ip_max = "SELECT count(*) AS `comment_total` FROM bg_comment WHERE `comment_ip`= %s AND `created_at` > %s"
    _comment_count = mysql_fetch_one(check_ip_max, (ip, yesterday_timestamp,))
    if _comment_count and _comment_count.get('comment_total') and int(_comment_count.get('comment_total')) > app.config.get('BLOG_COMMENT_MAX'):
        return make_response(jsonify({"code": 1, "message": "您一天内提交留言过多，服务端拒绝接收！"}))

    insert_sql="INSERT INTO bg_comment(`comment_post_id`, `comment_nickname`, `comment_site`, `comment_body`, `comment_ip`) VALUES(%s, %s, %s, %s, %s)"
    insert_kvs = (post_id, nickname, site, body, ip)
    mysql_execute(insert_sql, insert_kvs)

    return make_response(jsonify({"code": 0, "message":"您的留言已提交，请等待审核！"}))





