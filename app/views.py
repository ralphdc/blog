#!/usr/bin/env python3

from app import app, db
from flask import session, render_template, redirect, url_for, request, flash
from .forms import RegisterForm
from flask_login import logout_user, current_user, login_user
from .models import User


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
    return render_template('index.html')

@app.route('/admin')
def app_admin():
    return render_template('admin.html')

@app.route('/main')
def app_main():
    return render_template('main.html')

@app.route('/login')
def app_login():

    if current_user.is_authenticated:
        return redirect(url_for('app_admin'))


    return render_template('login.html')

@app.route('/logout')
def app_logout():
    logout_user()
    return redirect(url_for('app_login'))


@app.route('/register', methods=['GET', 'POST'])
def app_register():
    if session.get('loginTag'):
        return redirect(url_for('app_admin'))

    error = None
    form = RegisterForm(request.form)
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