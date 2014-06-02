# coding=utf-8
import os
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.permission import PermissionModel
from aireadManager.model import db

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)

permission_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tag': fields.String
}


def get_parser(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=unicode, required=required)
    parser.add_argument('tag', type=unicode, required=required)

    return parser


class Permissions(Resource):
    @marshal_with(permission_fields)
    def get(self):
        return PermissionModel.query.all()


class Permission(Resource):
    @marshal_with(permission_fields)
    def get(self, pid):
        return db.session.query(PermissionModel).filter_by(id=pid).first()


api.add_resource(Permissions, '/', endpoint='.permissions')
api.add_resource(Permission, '/<string:pid>', endpoint='.permission')
