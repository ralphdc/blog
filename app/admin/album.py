#!/usr/bin/env python3


from flask import request, render_template, make_response, jsonify, session
import datetime
from app import app, db, csrf
from app.models import Album, AlbumPhotoMap, Photo
from sqlalchemy import and_
from . import admin
from app.utils import *


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


    albums = db.session.query(Album.album_id, Album.album_name, Album.album_slt).filter(Album.album_status=='1').all()
    return render_template('album/index.html', albums=albums)


@admin.route('/album/show/<int:aid>', methods=['GET', 'POST'])
def admin_show(aid):

    if not aid:
        return make_response(jsonify({"code": 1, "message": "参数传递错误！"}))

    album = db.session.query(Album.album_name, Album.album_id).filter(Album.album_id==aid).first()

    query = db.session.query(
                                Album.album_name,
                                Album.album_creator,
                                Album.album_id,
                                Photo.photo_name,
                                Photo.photo_id,
                                Photo.photo_path
                             )\
            .outerjoin(AlbumPhotoMap, AlbumPhotoMap.album_id==Album.album_id)\
            .outerjoin(Photo, Photo.photo_id==AlbumPhotoMap.photo_id)\
            .filter(and_(Album.album_status=='1', Photo.photo_status=='1'))\
            .all()

    return render_template('album/lists.html', album=album, query=query)





#屏蔽csrf保护， 否则导致kindeditor上传失败！
@csrf.exempt
@app.route('/album/album_upload/<int:aid>', methods=['POST'])
def album_image_upload(aid=None):

    if not aid:
        return make_response(jsonify({"code": 1, "message": "相册参数未知，请联系管理员！"}))

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
        print(file_length)
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

        try:
            photoModal = Photo(
                photo_name=file_name,
                photo_upload_name=saved_file_name,
                photo_path=os.path.join(save_path, saved_file_name),
                photo_space=str(file_length),
                photo_creator=session['user']['user_name'],
            )
            db.session.add(photoModal)
            db.session.flush()
            albumMapModal = AlbumPhotoMap(
                album_id = aid,
                photo_id = photoModal.photo_id
            )
            db.session.add(albumMapModal)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
            return make_response(jsonify({"code": 1, "message": "数据库操作失败，请联系管理员！"}))
        finally:
            db.session.close()

        return make_response(jsonify({"error": 0, "url": "/cdn/{}".format(saved_file_name)}))
    else:
        return make_response(jsonify({"error": 1, "message": "[6]服务端未能检测到上传的文件对象，请选择文件！"}))

