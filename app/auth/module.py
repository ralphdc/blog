#!/usr/bin/env python3

from  flask import render_template, make_response, request, jsonify, session
from flask_login import current_user
from app import app, db
from app.models import User, UserAndRole, Role, RoleAndModule, Module
from sqlalchemy import and_
from . import auth



class getTreeInterface():

    def __init__(self):
        self.menu = []

    def getTreeInterface(self, mid=0):


        email = current_user.user_email
        menu = db.session.query(User.user_name, Module.module_id, Module.module_name, Module.module_parent) \
            .outerjoin(UserAndRole, UserAndRole.map_uid == User.user_id) \
            .outerjoin(Role, Role.role_id == UserAndRole.map_oid) \
            .outerjoin(RoleAndModule, Role.role_id == RoleAndModule.role_id) \
            .outerjoin(Module, Module.module_id == RoleAndModule.module_id) \
            .filter(and_(User.user_status == '1', Role.role_status == '1', Module.module_status == '1',
                         Module.module_parent == mid,
                         User.user_email == email)) \
            .all()

        if menu:
            for m in menu:
                mdict = {"name":m[2], "id": m[1], "pid": m[3]}
                self.menu.append(mdict)
                self.getTreeInterface(m[1])

    def getTreeNodes(self):

        self.getTreeInterface()

        return self.menu







@auth.route('/module', methods=['GET'])
def auth_module():

    return render_template('auth/module/index.html')


@auth.route('/tree', methods=['POST'])
def auth_tree():

    nodes = getTreeInterface()

    treeNodes = nodes.getTreeNodes()

    return make_response(jsonify(treeNodes))


@auth.route('/tree/create', methods=['POST'])
def auth_tree_create():

    module_name = request.form.get('module_name')
    module_url = request.form.get('module_url')
    module_status = request.form.get('module_status')
    module_icon = request.form.get('module_icon')
    module_description = request.form.get('module_description')
    module_parent = '0'


    if not module_name or not module_url:
        return make_response(jsonify({"code": 1, "message": "请填写菜单名称和URI访问地址！"}))

    try:
        module = Module(module_name, module_url, module_parent, module_status, module_icon,  module_description)
        db.session.add(module)
        db.session.flush()
        module_id = module.module_id
        db.session.commit()

    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()


    if module_id:
        try:
            db.session.add(RoleAndModule(session.get('role_id'), module_id))
            db.session.commit()
        except Exception as e:
            raise
        finally:
            db.session.close()
    else:
        return make_response(jsonify({"code": 1, "message": "数据库操作有误，请联系管理员！"}))

    return make_response(jsonify({"code": 0, "message": "新建成功！"}))


