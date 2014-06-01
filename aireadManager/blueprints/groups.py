# coding=utf-8
import os
from flask import abort, request
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.group import GroupModel
from aireadManager.model import db
from aireadManager.utils.errors import Code

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)

group_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tag': fields.String
}


def get_parser(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=unicode, required=required)
    parser.add_argument('tag', type=unicode, required=required)

    return parser


class Groups(Resource):
    @marshal_with(group_fields)
    def get(self):
        return GroupModel.query.all()

    def post(self):
        args = get_parser(required=True).parse_args()

        print 'args: ', args

        group = GroupModel(**args)
        db.session.add(group)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
            'uri': api.url_for(Group, gid=group.id)
        }

        return ret


class Group(Resource):
    @marshal_with(group_fields)
    def get(self, gid):
        return db.session.query(GroupModel).filter_by(id=gid).first()

    def post(self):
        abort(405)

    def put(self, gid):
        args = get_parser().parse_args()

        set_data = {key: val for key, val in args.iteritems() if val is not None}
        db.session.query(GroupModel).filter_by(id=gid).update(set_data)
        db.session.commit()

        ret = {
            'code': Code.SUCCESS,
        }
        return ret

    def delete(self, gid):
        db.session.query(GroupModel).filter_by(id=gid).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


api.add_resource(Groups, '/', endpoint='.groups')
api.add_resource(Group, '/<string:gid>', endpoint='.group')


