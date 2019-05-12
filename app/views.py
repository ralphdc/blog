#!/usr/bin/env python3

from app import app, db
from flask import session, render_template, redirect, url_for, request, flash, make_response, jsonify
from sqlalchemy import and_
from .forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .models import Visit
from .models import BoardUser, BoardContent
from .models import User, UserAndRole, Role, RoleAndModule, Module
from app.utils import getRandomKey

#递归，获取菜单项目；
def get_user_menu(mid=0, level=1):

    if level == 1:
        end_html = '</li>'
        endli = ''
        dataIndex = ''
        aClass = ''
        aTag = '<span class="fa arrow"></span>'
    else:
        dataIndex = 'data-index="{}"'.format(getRandomKey())
        end_html = '</ul>'
        endli = '</li>'
        aClass = 'class="J_menuItem"'
        aTag = ''

    email = current_user.user_email

    menu_html = ''

    menu = db.session.query(User.user_name, Module.module_id, Module.module_url, Module.module_name, Module.module_icon, Role.role_id) \
        .outerjoin(UserAndRole, UserAndRole.map_uid == User.user_id) \
        .outerjoin(Role, Role.role_id == UserAndRole.map_oid) \
        .outerjoin(RoleAndModule, Role.role_id == RoleAndModule.role_id) \
        .outerjoin(Module, Module.module_id == RoleAndModule.module_id) \
        .filter(and_(User.user_status == '1', Role.role_status == '1', Module.module_status == '1', Module.module_parent==mid, User.user_email == email)) \
        .all()

    if menu :
        if level == 1:
            menu_html += ''
        elif level == 2:
            menu_html += '<ul class="nav nav-second-level">'
        elif level == 3:
            menu_html += '<ul class="nav nav-third-level">'
        else:
            raise Exception("[Error] Currently menu level is limited to 3! ")

        level += 1
        for m in menu:
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

    if not current_user.is_authenticated:
        if request.is_xhr:
            return make_response(jsonify({"code": 1, "message": "请重新登录！"}))

@app.route('/')
def app_index():
    return render_template('index.html', navigate_active='index')

@app.route('/admin')
@login_required
def app_admin():
    #获取当前用户权限-菜单；
    user_menu = get_user_menu()
    return render_template('admin.html', menu=user_menu)


@app.route('/login', methods=['GET', 'POST'])
def app_login():
    session.permanent = True



    #pycharm重启导致Session失效，这里使用自动登录；
    '''
    UserModel = User.query.filter_by(user_email='472298551@qq.com').first()
    login_user(UserModel, remember='True')
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('app_admin')

    return redirect(next_page)
    '''







    if current_user.is_authenticated:
        return redirect(url_for('app_index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        UserModel = User.query.filter_by(user_email=email).first()

        if UserModel is None or not UserModel.check_password(password):
            flash("用户名或密码错误！")
            return redirect(url_for('app_login'))
        login_user(UserModel, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('app_admin')
        # add login history
        try:
            clientIP = request.remote_addr or '0.0.0.0'
            db.session.add(Visit(current_user.user_name, clientIP))
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            raise
        finally:
            db.session.close()

        try:
            RoleModule = db.session.query(User.user_name, Role.role_id) \
                .outerjoin(UserAndRole, UserAndRole.map_uid == User.user_id) \
                .outerjoin(Role, Role.role_id == UserAndRole.map_oid) \
                .filter(User.user_email == email) \
                .first()
        except Exception as e:
            raise
        finally:
            db.session.close()

        session['role_id'] = RoleModule[1]

        return redirect(next_page)
    elif form.errors:
        for field_name, errors in form.errors.items():
            for error in errors:
                flash("{0} - {1}".format(field_name, error), category='error')

    return render_template('login.html', form=form)

@app.route('/logout')
def app_logout():
    logout_user()
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
