#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, Length, EqualTo
from .models import User



class RegisterForm(FlaskForm):

    username = StringField(label='用户名', validators=[DataRequired(message="请输入用户名"), Length(6, 20, message="用户名长度不符合要求!")])
    email   =   StringField(label='邮件地址', validators=[DataRequired(message="请输入邮件地址"), Email(message="请使用正常的电子邮件格式！")])
    password = PasswordField(label='密码', validators=[DataRequired(message="请输入密码"), Length(7, 20, message="密码长度请保持在7到20之间")])
    repassword = PasswordField(label='确认密码', validators=[DataRequired(message="请确认密码"), EqualTo('password', message='密码和密码确认域的值需相同！')])
    blog = StringField(label='个人主页', validators=[DataRequired(message="请输入个人主页地址"), Length(1,255)])
    submit = SubmitField(label='注册')


    #判断username是否已经存在；
    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('Sorry! 用户名已存在！')

    #判断邮箱地址是否已经存在；
    def validate_email(self, email):
        user = User.query.filter_by(user_email=email.data).first()
        if user is not None:
            raise ValidationError('Sorry! 邮件地址已存在！')



class LoginForm(FlaskForm):

    email = StringField(label='电子邮件', validators=[DataRequired(message="请输入邮件地址"), Email(message="邮件地址格式错误！")])
    password = PasswordField(label='密码', validators=[DataRequired(message="请输入密码"), Length(7, 20, message="密码长度请保持在7到20之间")])
