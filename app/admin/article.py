#!/usr/bin/env python3

from flask import request, render_template, jsonify, session, make_response

from app.models import Category, User, Posts
from app import db, app, login_required
from app.utils import *
from . import admin
from sqlalchemy import and_, func


@login_required
@admin.route('/article', methods=['POST', 'GET'])
def article_index():

    if request.method == 'POST':
        search_posts_title = request.form.get('posts_title')
        # 页面容量；
        limit = request.form.get('limit') or app.config.get('PAGE_LIMIT')
        # 页码；
        offset = request.form.get('offset') or app.config.get('PAGE_OFFSET')

        limit = int(limit)
        offset = int(offset)
        try:
            qy = db.session.query(Posts.posts_id, Posts.posts_title, Posts.posts_status, Posts.posts_allow, Posts.created_at, Posts.posts_comment, Posts.posts_visit)\
                .filter(Posts.posts_creator==session['user']['user_name'])

            if search_posts_title:
                qy = qy.filter(Posts.posts_title.like('%{}%'.format(search_posts_title.strip())))

            count = db.session.query(func.count(Posts.posts_id)).filter(Posts.posts_creator==session['user']['user_name']).scalar()
            qy = qy.limit(limit).offset(offset)
            qy = qy.all()
        except Exception as e:
            raise
        finally:
            db.session.close()

        if qy:
            title = ('posts_id', 'posts_title', 'posts_status', 'posts_allow', 'created_at', 'posts_comment', 'posts_visit')
            rows = make_row(title, qy)
            return make_response(jsonify({"code": 0, "message": "SUCCESS", "rows": rows, "total": count}))
        else:
            return make_response(jsonify({"code": 1, "message": "查询结果为空！"}))

    return render_template('article/index.html')


@login_required
@admin.route('/article/add', methods=['POST', 'GET'])
@admin.route('/article/add/<int:pid>', methods=['GET'])
def article_add(pid=None):
    posts = None
    if request.method == 'POST':
        posts_id = request.form.get('posts_id')
        posts_title = request.form.get('posts_title')
        posts_desc = request.form.get('posts_desc') or None
        posts_content = request.form.get('posts_content')
        posts_status = request.form.get('posts_status') or '1'
        posts_category = request.form.get('posts_real_category')
        posts_allow = request.form.get('posts_allow')  or '1'
        posts_password = request.form.get('posts_password')
        posts_top = request.form.get('posts_top') or '0'
        posts_tag = request.form.get('posts_tag') or '' 
        posts_seo = request.form.get('posts_seo') or ''

        if not posts_title or not posts_content:
            return make_response(jsonify({"code": 1, "message": "请填写文章标题和内容！"}))

        if posts_id:
            #edit article;
            update_posts = db.session.query(Posts).filter(Posts.posts_id==posts_id).first()

            if update_posts:
                try:
                    update_posts.posts_title = posts_title
                    update_posts.posts_desc = posts_desc
                    update_posts.posts_content = posts_content
                    update_posts.posts_status = posts_status
                    update_posts.posts_allow = posts_allow
                    update_posts.posts_top = posts_top
                    update_posts.posts_category = posts_category
                    update_posts.posts_tag = posts_tag
                    update_posts.posts_seo = posts_seo

                    if posts_password:
                        update_posts.set_password(posts_password)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    app.logger.exception(e)
                    return make_response(jsonify({"code": 1, "message": "更新失败,请联系管理员！"}))
                finally:
                    db.session.close()
                return make_response(jsonify({"code": 0, "message": "更新成功！"}))
        else:
            #insert posts
            try:
                posts = Posts(
                    posts_title=posts_title,
                    posts_desc=posts_desc,
                    posts_content=posts_content,
                    posts_status=posts_status,
                    posts_allow=posts_allow,
                    posts_top=posts_top,
                    posts_creator=session['user']['user_name'],
                    posts_category = posts_category,
                    posts_tag = posts_tag,
                    posts_seo = posts_seo
                )

                if posts_password:
                    posts.set_password(posts_password)

                db.session.add(posts)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise
                return make_response(jsonify({"code": 1, "message": "文章入库操作失败，请联系管理员！"}))
            finally:
                db.session.close()

        return make_response(jsonify({"code": 0, "message": "提交成功！"}))

    else:
        #edit
        if pid:
            posts = db.session.query(
                Posts.posts_id,
                Posts.posts_title,
                Posts.posts_desc,
                Posts.posts_content,
                Posts.posts_status,
                Posts.posts_allow,
                Posts.posts_top,
                Posts.posts_category,
                Posts.posts_tag,
                Posts.posts_seo)\
                .filter(Posts.posts_id==pid).first()

        #获取文章分类；
        category = db.session.query(Category.category_id, Category.category_content) \
            .outerjoin(User, User.user_id == Category.category_creator) \
            .filter(and_(User.user_name == session['user']['user_name']), Category.category_status=='1')\
            .all()
        selected_category = [ int(x) for x in posts[7].split(',') ] if posts and posts[7] else []
        return render_template('article/add.html', category=category, posts=posts, selected_category=selected_category )

@login_required
@admin.route('/article/delete', methods=['POST'])
def article_delete():
    pid = request.form.get('pid')
    if not pid:
        return make_response(jsonify({"code": 1, "message": "参数传递错误，请联系管理员！"}))
    try:
        posts = db.session.query(Posts).filter(Posts.posts_id==pid).first()
        if posts:
            db.session.delete(posts)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()
    return make_response(jsonify({"code": 0, "message": "删除成功！"}))