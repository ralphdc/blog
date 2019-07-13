#!/usr/bin/env python3

from flask import render_template, make_response, jsonify, session, request
from sqlalchemy import and_, func
from app import app, db
from app.utils import *
from app.models import BoardContent, BoardUser
from . import admin


@admin.route('/comment', methods=['POST', 'GET'])
def admin_comment():

    if request.method == 'POST':
        board_user = request.form.get('board_user')

        # 页面容量；
        limit = request.form.get('limit') or app.config.get('PAGE_LIMIT')
        # 页码；
        offset = request.form.get('offset') or app.config.get('PAGE_OFFSET')

        limit = int(limit)
        offset = int(offset)

        try:
            qy = db.session.query(
                                    BoardContent.board_content_body,
                                    BoardContent.board_content_type,
                                    BoardContent.board_content_status,
                                    BoardContent.created_at,
                                    BoardUser.board_user_nickname,
                                    BoardUser.board_user_status,
                                    BoardUser.board_user_email,
                                    BoardUser.board_user_url
                                  )\
            .outerjoin(BoardUser, BoardUser.board_user_id==BoardContent.board_content_uid)\

            if board_user:
                qy = qy.filter(BoardUser.board_user_nickname==board_user)

            count = qy.count()
            qy = qy.limit(limit).offset(offset)
            qy = qy.all()
        except Exception as e:
            raise
        finally:
            db.session.close()

        if qy:
            title = ('board_content_body', 'board_content_type','board_content_status', 'created_at', 'board_user_nickname', 'board_user_status', 'board_user_email', 'board_user_url')
            rows = make_row(title, qy)
            return make_response(jsonify({"code": 0, "message": "SUCCESS", "rows": rows, "total": count}))
        else:
            return make_response(jsonify({"code": 1, "message": "查询结果为空！"}))


    return render_template('comment/index.html')


