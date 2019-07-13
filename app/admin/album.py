#!/usr/bin/env python3


from flask import request, render_template, make_response, jsonify, session
from app import app, db
from app.models import Album
from . import admin


@admin.route('/album', methods=['GET', 'POST'])
def admin_album():

    if request.method == 'POST':

        album_name = request.form.get('album_name')
        album_state = request.form.get('album_state') or '1'
        album_desc = request.form.get('album_desc')

        if not album_name:
            return make_response(jsonify({"code": 1, "message": "请填写相册名称！"}))
        try:
            db.session.add(Album(album_name=album_name, album_desc=album_desc))
            db.session.commit()
        except Exception:
            db.rollback()
            return make_response(jsonify({"code": 1, "message": "新增失败，请联系管理员！"}))
        finally:
            db.session.close()
        return make_response(jsonify({"code": 0, "message": "新建成功！"}))



    albums = db.session.query(Album.album_name, Album.album_slt, Album.created_at).all()

    return render_template('album/index.html', albums=albums)

