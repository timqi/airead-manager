# coding=utf-8
import os
from flask import abort
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.user_group import UserGroupModel
from aireadManager.model import db
from aireadManager.utils.errors import Code

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)

user_group_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'group_id': fields.Integer,
}


def get_parser(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=required)
    parser.add_argument('group_id', type=int, required=required)

    return parser


class UserGroups(Resource):
    @marshal_with(user_group_fields)
    def get(self):
        return UserGroupModel.query.all()

    def post(self):
        args = get_parser(required=True).parse_args()

        print 'args: ', args

        user_group = UserGroupModel(**args)
        db.session.add(user_group)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
            'uri': api.url_for(UserGroup, ugid=user_group.id)
        }

        return ret


class UserGroup(Resource):
    @marshal_with(user_group_fields)
    def get(self, ugid):
        return db.session.query(UserGroupModel).filter_by(id=ugid).first()

    def post(self):
        abort(405)

    def put(self, ugid):
        args = get_parser().parse_args()

        set_data = {key: val for key, val in args.iteritems() if val is not None}
        db.session.query(UserGroupModel).filter_by(id=ugid).update(set_data)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
        }
        return ret

    def delete(self, ugid):
        db.session.query(UserGroupModel).filter_by(id=ugid).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


class UserGroupDelete(Resource):
    def post(self):
        abort(405)

    def delete(self, user_id, group_id):
        db.session.query(UserGroupModel).filter_by(
            user_id=user_id).filter_by(group_id=group_id).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


api.add_resource(UserGroups, '/', endpoint='.user_groups')
api.add_resource(UserGroup, '/<string:ugid>', endpoint='.user_group')
api.add_resource(UserGroupDelete, '/<int:user_id>/<int:group_id>', endpoint='./user_group_delete')
