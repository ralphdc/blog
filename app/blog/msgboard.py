#!/usr/bin/env python3

from flask import render_template, make_response, jsonify, request, flash, redirect, url_for
from . import blog
from app.forms import MsgBoardForm
from app import app,db
from sqlalchemy import and_
from app.models import BoardUser, BoardContent
import pytz
import arrow
import datetime, time
tz = pytz.timezone("Asia/Shanghai")



@blog.route('/msgboard', methods=['GET', 'POST'])
def msgboard_index():

    form  = MsgBoardForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        email = form.email.data
        blog = form.blog.data
        content = form.board_content.data
        ip = request.remote_addr
        comment_type = form.commentType.data or '1'
        comment_target = form.commentTarget.data or None
        query_user = db.session.query(BoardUser.board_user_id).filter(BoardUser.board_user_email==email).first()

        if query_user:
            uid = query_user[0]
            last_created = db.session.query(BoardContent.created_at).filter(BoardContent.board_content_uid==uid).order_by(BoardContent.created_at.desc()).first()
            if last_created:
                current_timestamp = int(time.time())
                last_timestamp = int(time.mktime(time.strptime(str(last_created[0]), "%Y-%m-%d %H:%M:%S")))
                interval = int((current_timestamp - last_timestamp)/60)
                #5分钟内不允许重复留言；
                if interval < app.config.get('BOARD_COMMENT_TIME_LIMIT'):
                    flash("您的留言评论过于频繁，请{}分钟后再试！".format(app.config.get('BOARD_COMMENT_TIME_LIMIT')))
                    return redirect(url_for('blog.msgboard_index'))
        else:
            try:
                board_user = BoardUser(nickname, email, blog, ip)
                db.session.add(board_user)
                db.session.flush()
                uid = board_user.board_user_id
                db.session.commit()
            except Exception as e:
                app.logger.exception(e)
                db.session.rollback()
            finally:
                db.session.close()
        if uid:
            try:
                board_content = BoardContent(uid, content, comment_type, comment_target)
                db.session.add(board_content)
                db.session.commit()
                flash('留言已成功提交,请等待审核！')
                return redirect(url_for('blog.msgboard_index'))
            except Exception as e:
                app.logger.exception(e)
                db.session.rollback()
            finally:
                db.session.close()
        else:
            app.logger.error('BoardUser table insert failed......')
            flash("您的留言提交失败， 请稍后再试！")

    elif form.errors:
        for field_name, errors in form.errors.items():
            for error in errors:
                flash("{0} - {1}".format(field_name, error), category='error')


    #查询留言（加分页）
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(
                    BoardContent.board_content_id,
                    BoardContent.board_content_body,
                    BoardContent.created_at,
                    BoardUser.board_user_nickname
                    )\
                    .outerjoin(BoardUser, BoardUser.board_user_id==BoardContent.board_content_uid)\
                    .filter(and_(BoardContent.board_content_status=='1', BoardUser.board_user_status=='1', BoardContent.board_content_type=='1'))\
                    .order_by(BoardContent.created_at.desc())\
                    .paginate(page, per_page=app.config.get('FLASKY_POST_PER_PAGE'), error_out=False)


    boards = pagination.items
    return render_template('msgboard/index.html', navigate_active='msgboard', form=form, paginate=pagination, boards=boards, endpoint='blog.msgboard_index')


