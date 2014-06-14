# coding=utf-8
import os
from flask import abort
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.permissions import Permissions
from aireadManager.utils.restful import Resource
from aireadManager.model.group_permission import GroupPermissionModel
from aireadManager.model import db
from aireadManager.utils.errors import Code

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)

group_permission_fields = {
    'id': fields.Integer,
    'group_id': fields.Integer,
    'permission_id': fields.Integer
}


def get_parser(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('group_id', type=int, required=required)
    parser.add_argument('permission_id', type=int, required=required)

    return parser


class GroupPermissions(Resource):
    @marshal_with(group_permission_fields)
    def get(self):
        return GroupPermissionModel.query.all()

    @Permissions.admin.require(403)
    def post(self):
        args = get_parser(required=True).parse_args()

        group_perm = GroupPermissionModel(**args)
        db.session.add(group_perm)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
            'uri': api.url_for(GroupPermission, gpid=group_perm.id)
        }

        return ret


class GroupPermission(Resource):
    @marshal_with(group_permission_fields)
    def get(self, gpid):
        return db.session.query(GroupPermissionModel).filter_by(id=gpid).first()

    @Permissions.admin.require(403)
    def post(self):
        abort(405)

    @Permissions.admin.require(403)
    def put(self, gpid):
        args = get_parser().parse_args()

        set_data = {key: val for key, val in args.iteritems() if val is not None}
        db.session.query(GroupPermissionModel).filter_by(id=gpid).update(set_data)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
        }
        return ret

    @Permissions.admin.require(403)
    def delete(self, gpid):
        db.session.query(GroupPermissionModel).filter_by(id=gpid).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


class GroupPermissionDelete(Resource):
    @Permissions.admin.require(403)
    def post(self):
        abort(405)

    @Permissions.admin.require(403)
    def delete(self, group_id, perm_id):
        db.session.query(GroupPermissionModel).filter_by(
            group_id=group_id).filter_by(permission_id=perm_id).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}



api.add_resource(GroupPermissions, '/', endpoint='.group_permissions')
api.add_resource(GroupPermission, '/<string:gpid>', endpoint='.group_permission')
api.add_resource(GroupPermissionDelete, '/<int:group_id>/<int:perm_id>', endpoint='./user_group_delete')
