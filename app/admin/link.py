#!/usr/bin/env python3

from flask import render_template, make_response, jsonify, request, session

from app.utils import *
from app import db, app
from app.models import OuterLink
from sqlalchemy import func
from . import admin


@admin.route('/link', methods=['GET', 'POST'])
def link_index():
    if request.method == 'POST':
        link_name = request.form.get('link_name')
        # 页面容量；
        limit = request.form.get('limit') or app.config.get('PAGE_LIMIT')
        # 页码；
        offset = request.form.get('offset') or app.config.get('PAGE_OFFSET')

        limit = int(limit)
        offset = int(offset)

        qy = db.session.query(
                              OuterLink.link_id,
                              OuterLink.link_name,
                              OuterLink.link_href,
                              OuterLink.link_desc,
                              OuterLink.link_email,
                              OuterLink.link_mobile,
                              OuterLink.created_at
                              )
        if link_name:
            qy = qy.filter(OuterLink.link_name == link_name)
        count = db.session.query(func.count(OuterLink.link_id)).scalar()
        qy = qy.limit(limit).offset(offset)
        qy = qy.all()

        if qy:
            title = ('link_id','link_name', 'link_href', 'link_desc', 'link_email', 'link_mobile', 'created_at')
            rows = make_row(title, qy)
            return make_response(jsonify({"code": 0, "message": "SUCCESS", "rows": rows, "total": count}))
        else:
            return make_response(jsonify({"code": 1, "message": "查询数据库失败！"}))
    else:
        return render_template('link/index.html')



@admin.route('/link/add', methods=['POST'])
def link_add():
    edit_id = request.form.get('edit_id')
    modal_link_name = request.form.get('modal_link_name')
    modal_link_href = request.form.get('modal_link_href')
    modal_link_desc = request.form.get('modal_link_desc')
    modal_link_email = request.form.get('modal_link_email')
    modal_link_mobile = request.form.get('modal_link_mobile')

    if not modal_link_name or not modal_link_href:
        return make_response(jsonify({"code":1, "message": "请填写连接名称和连接地址！"}))

    if edit_id:
        #edit
        try:
            db.session.query(OuterLink).filter(OuterLink.link_id==edit_id).update({
                "link_name": modal_link_name,
                "link_href": modal_link_href,
                "link_desc": modal_link_desc,
                "link_email":modal_link_email,
                "link_mobile":modal_link_mobile
            })
            db.session.commit()
        except Exception :
            return make_response(jsonify({"code": 1, "message": "数据更新失败，请联系管理员！"}))
            db.session.rollback()
        finally:
            db.session.close()
        return make_response(jsonify({"code": 0, "message": "更新成功！"}))

    else:
        #add
        try:
            linkModal = OuterLink(
                link_name=modal_link_name,
                link_href = modal_link_href,
                link_desc = modal_link_desc,
                link_email = modal_link_email,
                link_mobile = modal_link_mobile
            )
            db.session.add(linkModal)
            db.session.commit()
            return make_response(jsonify({"code": 0, "message": "提交成功"}))
        except Exception as e:
            app.logger.exception(e)
            return make_response(jsonify({"code": 1, "message": "执行错误，请联系管理员！"}))



@admin.route('/link/query/<int:kid>', methods=['POST', 'GET'])
def link_query(kid):


    if not kid:
        return make_response(jsonify({"code":1, "message": "参数传递错误！"}))

    ky = db.session.query(
        OuterLink.link_name,
        OuterLink.link_href,
        OuterLink.link_desc,
        OuterLink.link_email,
        OuterLink.link_mobile
    ).\
        filter(OuterLink.link_id==kid).first()
    if ky :
        title = ('link_name', 'link_href', 'link_desc', 'link_email', 'link_mobile')
        rows = make_row(title, [ ky ])
        return make_response(jsonify({"code":0, "data": rows, "message": "查询成功！"}))
    else:
        return make_response(jsonify({"code": 1,  "message": "查询失败！"}))


@admin.route('/category/delete', methods=['POST'])
def link_delete():

    cid = request.form.get('cid')

    if not cid:
        return make_response(jsonify({"code": 1, "message": "参数传递错误！"}))

    try:
        cid = int(cid)
    except Exception:
        return make_response(jsonify({"code":1, "message": "参数转换错误！请通知管理员！"}))

    try:
        db.session.query(Category).filter(Category.category_id==cid).delete()
        db.session.commit()
    except Exception:
        return make_response(jsonify({"code": 1, "message": "删除失败！请通知管理员！"}))
    finally:
        db.session.close()

    return make_response(jsonify({"code": 0, "message": "删除成功！"}))