#!/usr/bin/env python3

from  flask import render_template, make_response, request, jsonify, session
from app import app, db
from app.models import User, UserAndRole, Role, RoleAndModule, Module
from sqlalchemy import and_, func
from . import admin



class getTreeInterface():

    def __init__(self):
        self.menu = []

    def getTreeInterface(self, mid=0):


        email = session.get('user').get('user_email')
        menu = db.session.query(User.user_name, Module.module_id, Module.module_name, Module.module_parent, Module.created_at) \
            .outerjoin(UserAndRole, UserAndRole.map_uid == User.user_id) \
            .outerjoin(Role, Role.role_id == UserAndRole.map_oid) \
            .outerjoin(RoleAndModule, Role.role_id == RoleAndModule.role_id) \
            .outerjoin(Module, Module.module_id == RoleAndModule.module_id) \
            .filter(and_(User.user_status == '1', Role.role_status == '1', Module.module_parent == mid,User.user_email == email)) \
            .order_by(Module.created_at.desc()) \
            .all()
        if menu:
            for m in menu:
                mdict = {"name":m[2], "id": m[1], "pid": m[3]}
                self.menu.append(mdict)
                self.getTreeInterface(m[1])

    def getTreeNodes(self):

        self.getTreeInterface()

        return self.menu



@admin.route('/auth/module', methods=['GET'])
def auth_module():

    return render_template('auth/module/index.html')


@admin.route('/auth/tree', methods=['POST'])
def auth_tree():

    nodes = getTreeInterface()

    treeNodes = nodes.getTreeNodes()

    return make_response(jsonify(treeNodes))


@admin.route('/auth/tree/create', methods=['POST'])
def auth_tree_create():

    module_id = request.form.get('module_id')
    module_name = request.form.get('module_name')
    module_url = request.form.get('module_url')
    module_status = request.form.get('module_status')
    module_icon = request.form.get('module_icon')
    module_description = request.form.get('module_description')
    module_parent = request.form.get('module_parent')

    #create new node;
    if not module_id:
        if not module_name or not module_url or not module_parent or not module_status:
            return make_response(jsonify({"code": 1, "message": "提交数据不完整，请检查！"}))
        try:
            module = Module(module_name, module_url, module_parent, module_status, module_icon,  module_description)
            db.session.add(module)
            db.session.commit()
            module_id = module.module_id
        except Exception as e:
            app.logger.exception(e)
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

    #edit node
    else:
        if not module_name or not module_url or not module_status:
            return make_response(jsonify({"code": 1, "message": "提交数据不完整，请检查！"}))

        try:
            db.session.query(Module).filter(Module.module_id==module_id).update({

                'module_name': module_name,
                'module_url': module_url,
                'module_status': module_status,
                'module_icon': module_icon,
                'module_description': module_description
            })
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            db.session.rollback()
        finally:
            db.session.close()
    return make_response(jsonify({"code": 0, "message": "操作成功！"}))


@admin.route('/auth/delete', methods=['GET', 'POST'])
def auth_delete_node():

    nid = request.form.get('nid')
    if not nid:
        return make_response(jsonify({"code":1, "message":"参数传递错误！"}))

    query = db.session.query(func.count(Module.module_id)).filter(Module.module_parent==nid).scalar()

    if query:
        return make_response(jsonify({"code":1, "message": "请删除节点下面的子节点先！"}))

    try:
        db.session.query(RoleAndModule).filter(RoleAndModule.module_id==nid).delete()
        db.session.query(Module).filter(Module.module_id==nid).delete()
        db.session.commit()
        return make_response(jsonify({"code":0, "message":"删除成功！"}))
    except Exception :
        db.rollback()
        return make_response(jsonify({"code": 1, "message": "数据库执行失败，请联系管理员！"}))
    finally:
        db.session.close()


@admin.route('/auth/query/<int:nid>', methods=['GET'])
def auth_query(nid):

    if not nid:
        return make_response(jsonify({"code": 1, "message": "参数传递错误！"}))

    nodeInfo = db.session.query(
        Module.module_id,
        Module.module_parent,
        Module.module_name,
        Module.module_url,
        Module.module_description,
        Module.module_icon,
        Module.module_status
    ) \
    .filter(Module.module_id==nid)\
    .first()
    if not nodeInfo:
        return make_response(jsonify({"code":1, "message":"节点不存在！"}))

    parentName = '/'

    if int(nodeInfo[0]) > 0:
        nodeParentInfo = db.session.query(
            Module.module_name
        )\
        .filter(Module.module_id==nodeInfo[0])\
        .first()

        if nodeParentInfo:
            parentName = nodeParentInfo[0]

    nodeInfo = list(nodeInfo)
    nodeInfo.append(parentName)
    title = ['module_id','module_parent', 'module_name', 'module_url', 'module_description', 'module_icon', 'module_status', 'module_parent_name']
    return make_response(jsonify({"code":0, "message":"查询成功！", "data": dict(zip(title, nodeInfo))}))