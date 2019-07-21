#!/usr/bin/env python3

from app import app, db
from flask import session, render_template, redirect, url_for, request, flash, make_response, jsonify
from sqlalchemy import and_
from .forms import RegisterForm, LoginForm
from werkzeug.urls import url_parse
from .models import Visit
from .models import BoardUser, BoardContent
from .models import User, UserAndRole, Role, RoleAndModule, Module
from app.utils import *
from app import rdx
from app import csrf
import json
import functools


def login_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        ukey = None
        if session.get('user'):
            ukey = session.get('user').get('ukey')
        if not ukey:
            ukey = request.cookies.get('ukey')
        if not ukey or not redis_get(ukey):
            if request.is_xhr:
                return make_response(jsonify({"code": 1, "message": "请重新登录！"}))
            else:
                return redirect(url_for('app_login'))
        return func(*args, **kwargs)
    return decorator


#递归，获取菜单项目；
def get_user_menu(mid=0, level=1):

    if level == 1:
        end_html = '</li>'
        endli = ''
        aTag = '<span class="fa arrow"></span>'
    else:
        end_html = '</ul>'
        endli = '</li>'
        aTag = ''

    email = session['user']['user_email']

    menu_html = ''

    menu = db.session.query(User.user_name, Module.module_id, Module.module_url, Module.module_name, Module.module_icon, Role.role_id) \
        .outerjoin(UserAndRole, UserAndRole.map_uid == User.user_id) \
        .outerjoin(Role, Role.role_id == UserAndRole.map_oid) \
        .outerjoin(RoleAndModule, Role.role_id == RoleAndModule.role_id) \
        .outerjoin(Module, Module.module_id == RoleAndModule.module_id) \
        .filter(and_(User.user_status == '1', Role.role_status == '1', Module.module_status == '1', Module.module_parent==mid, User.user_email == email)) \
        .order_by(Module.created_at.desc()) \
        .all()

    if menu :
        if level == 1:
            menu_html += ''
        else:
            menu_html += '<ul class="nav nav-{}-level">'.format(level)

        level += 1
        for m in menu:
            aClass = '' if not m[2].startswith('/') else 'class="J_menuItem"'
            dataIndex = '' if not m[2].startswith('/') else 'data-index="{}"'.format(getRandomKey())
            menu_html += '<li><a {} href="{}" {}> <i class="{}"></i> <span class="nav-label">{}</span> {} </a>{}'.format(aClass, m[2], dataIndex, m[4],  m[3],  aTag, endli)
            menu_html += get_user_menu(m[1], level)

        menu_html += end_html

    return menu_html

@app.before_request
def before_request():

    if not session.get('title'):
        session['title'] = app.config.get('BLOG_TITLE')
    if not session.get('keywords'):
        session['keywords'] = app.config.get('BLOG_KEYWORDS')
    if not session.get('description'):
        session['description'] = app.config.get('BLOG_CONTENT')
    if not session.get('header'):
        session['header'] = app.config.get('BLOG_HEADER')


@app.route('/')
def app_index():
    return render_template('index.html', navigate_active='index')


@app.route('/admin')
@login_required
def app_admin():
    #获取当前用户权限-菜单；
    user_menu = get_user_menu()
    resp = make_response(render_template('admin.html', menu=user_menu))
    resp.set_cookie('ukey', session['user']['ukey'], max_age=app.config.get('COOKIE_MAX_AGE'))
    resp.headers['blogTag'] = 'Hello World'
    return resp


@app.route('/login', methods=['GET', 'POST'])
def app_login():


    #pycharm重启导致Session失效，这里使用自动登录；
    '''
    UserModel = User.query.filter_by(user_email='472298551@qq.com').first()
    login_user(UserModel, remember='True')
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('app_admin')

    return redirect(next_page)
    '''

    ukey = None
    if session.get('user'):
        ukey = session.get('user').get('ukey')
    if not ukey:
        ukey = request.cookies.get('ukey')

    if ukey and  redis_get(ukey):
        return redirect(url_for('app_admin'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        UserModel = User.query.filter_by(user_email=email).first()

        if UserModel is None or not UserModel.check_password(password):
            flash("用户名或密码错误！")
            return redirect(url_for('app_login'))

        #设置登录；
        user_name = UserModel.get_user_name()
        user_id = UserModel.get_user_id()
        user_email = UserModel.get_user_email()
        ukey = get_user_key(user_name)
        session['user'] = dict()
        session['user']['ukey'] = ukey
        session['user']['user_name'] = user_name
        session['user']['user_id'] = user_id
        session['user']['user_email'] = user_email
        session.permanent = True
        uvalue = {'user_name': user_name, 'user_id':user_id, 'user_email': user_email}
        redis_set(ukey, json.dumps(uvalue))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('app_admin')
        # add login history

        try:
            clientIP = request.remote_addr or '0.0.0.0'
            db.session.add(Visit(user_name, clientIP))
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            raise
        finally:
            db.session.close()
        return redirect(next_page)

    elif form.errors:
        for field_name, errors in form.errors.items():
            for error in errors:
                flash("{0} - {1}".format(field_name, error), category='error')

    return render_template('login.html', form=form)

@app.route('/logout')
def app_logout():
    rdx.delete(session['user']['ukey'])
    return redirect(url_for('app_login'))


@app.route('/register', methods=['GET', 'POST'])
def app_register():
    if session.get('loginTag'):
        return redirect(url_for('app_admin'))

    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User(
                            form.username.data.strip(),
                            form.password.data.strip(),
                            form.email.data.strip(),
                            form.blog.data.strip()
                        )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.session.close()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('app_admin'))

    elif form.errors:
        for field_name, errors in form.errors.items():
            for error in errors:
                flash("{0} - {1}".format(field_name, errors), category='error')
    return render_template('register.html', form=form, error=error)

#屏蔽csrf保护， 否则导致kindeditor上传失败！
@csrf.exempt
@app.route('/image_upload', methods=['POST'])
def app_image_upload():

    import os
    if not app.config.get('UPLOAD_FILE_PATH'):
        return make_response(jsonify({"error": 1, "message": "[0]服务器端未能正确设置上传目录，请通知管理员！"}))

    if not os.path.exists(app.config.get('UPLOAD_FILE_PATH')):
        try:
            os.makedirs(app.config.get('UPLOAD_FILE_PATH'))
        except Exception as e:
            return make_response(jsonify({"error": 1, "message": "[1]服务器端创建目录失败，请通知管理员！"}))

    item_dir = request.args.get('dir').strip() if request.args.get('dir')  else 'image'
    if not item_dir in app.config.get('UPLOAD_FILE'):
        return make_response(jsonify({"error": 1, "message": "[2]上传文件类型错误！"}))

    save_path = os.path.join(app.config.get('UPLOAD_FILE_PATH'), item_dir)
    save_path += '/'
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
        except Exception as e:
            return make_response(jsonify({"error": 1, "message": str(e)}))
    upload_file = request.files.get('imgFile')
    if upload_file:
        file_name = upload_file.filename
        file_length = len(upload_file.read())
        if not file_name or not file_length or not "." in file_name:
            return make_response(jsonify({"error": 1, "message": "[3]请检查上传文件的名称和大小！"}))

        if file_length > app.config.get('MAX_CONTENT_LENGTH'):
            return make_response(jsonify({"error": 1, "message": "[4]上传文件大小超出限制，服务端拒绝接收！"}))

        suffix = file_name.split(".")[-1]
        if not suffix.lower() in app.config.get('UPLOAD_FILE').get(item_dir):
            return make_response(jsonify({"error": 1, "message": "[5]上传文件类型错误！"}))
        saved_file_name = "{}.{}".format(getRandomKey(), suffix)
        try:
            #读取后，执行下这个就可以了
            # 重新定义指针到文件开头
            upload_file.seek(0)
            upload_file.save(os.path.join(save_path, saved_file_name))
        except Exception as e:
            raise
            return make_response(jsonify({"error": 1, "message": str(e)}))
        return make_response(jsonify({"error": 0, "url": "/cdn/{}".format(saved_file_name)}))
    else:
        return make_response(jsonify({"error": 1, "message": "[6]服务端未能检测到上传的文件对象，请选择文件！"}))




#查询留言的回复内容；
@app.template_filter('get_reply')
def get_reply(id, level):

    html = ''
    level += 1

    reply = db.session.query(
            BoardContent.board_content_body,
            BoardContent.created_at,
            BoardContent.board_content_id,
            BoardUser.board_user_nickname
        ) \
        .outerjoin(BoardUser, BoardUser.board_user_id == BoardContent.board_content_uid)\
        .filter(
                BoardUser.board_user_status == '1',
                BoardContent.board_content_status == '1',
                BoardContent.board_content_type == '2',
                BoardContent.board_content_target == id
        )\
        .all()

    if reply:
        html = '<ul class="children">'
        for rep in reply:
            html += ("<li class='depth-%s'>" % level)
            html += '''
                <div class="comment-info">
                    <img alt="" src="images/gravatar.jpg" class="avatar" height="40" width="40"> 
                    <cite> 
                        <a href="#">%s</a> Says: <br>
                        <span class="comment-data"><a href="#">%s</a> </span> 
                    </cite>
                </div>
                <div class="comment-text">
                    <p>%s</p>
                    <div class="reply"> <a class="comment-reply-link" href="#commentForm" onclick="give_replay(%d)">回复</a> </div>
				</div>
            ''' % (rep[3], rep[1], rep[0], rep[2])

            for_reply = get_reply(rep[2], level)
            if for_reply:
                html += for_reply

            html += "</li>"
        html += "</ul>"

    return html


