#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import URLField
from wtforms.validators import url
from .models import User, BoardUser



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

    email = StringField(label='电子邮件:', validators=[DataRequired(message="请输入邮件地址"), Email(message="邮件地址格式错误！")])
    password = PasswordField(label='密码:', validators=[DataRequired(message="请输入密码"), Length(7, 20, message="密码长度请保持在7到20之间")])
    remember_me = BooleanField(label='remember_me')
    submit = SubmitField(label='登录')



class MsgBoardForm(FlaskForm):
    nickname    = StringField(label='昵称：', validators=[DataRequired(message='请输入昵称!'), Length(5, 10, message='昵称长度请在5-10之间')])
    email       = StringField(label='邮箱地址：', validators=[DataRequired(message='请输入邮箱地址!'), Email(message='请输入正确的电子邮件地址')])
    blog        = URLField(label='个人主页：', validators=[url(message='URL地址错误！')])
    board_content     = TextAreaField(label='留言内容：', validators=[DataRequired(message='请填写留言内容！')])
    commentType = HiddenField (label='评论类型', validators=[DataRequired(message='无法确定您提交的是评论还是回复!')], default='1')
    commentTarget = HiddenField (label='回复对象', validators=[])
    submit = SubmitField(label='提交')

