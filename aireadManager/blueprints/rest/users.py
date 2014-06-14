import os
from flask import abort, request
from flask import g
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.user import UserModel
from aireadManager.model import db
from aireadManager.utils.errors import Code
from aireadManager.utils.util import datetime_type, get_string_from_datetime, bool_type
from datetime import datetime
from aireadManager.utils.permissions import Permissions

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'is_staff': fields.Boolean,
    'is_active': fields.Boolean,
    'is_superuser': fields.Boolean,
    'last_login': fields.DateTime,
    'date_joined': fields.DateTime,
}


def get_parser(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=unicode, required=required)
    parser.add_argument('first_name', type=unicode, required=required)
    parser.add_argument('last_name', type=unicode, required=required)
    parser.add_argument('email', type=str, required=required)
    parser.add_argument('password', type=str, required=required)
    parser.add_argument('is_staff', type=bool_type, required=required)
    parser.add_argument('is_active', type=bool_type, required=required)
    parser.add_argument('is_superuser', type=bool_type, required=required)
    parser.add_argument('last_login', type=datetime_type)

    return parser


class Users(Resource):
    @Permissions.admin.require(403)
    @marshal_with(user_fields)
    def get(self):
        return UserModel.query.all()

    @Permissions.admin.require(403)
    def post(self):
        print request.form
        args = get_parser(required=True).parse_args()

        args['date_joined'] = datetime.now()
        if not args['last_login']:
            args['last_login'] = datetime.now()

        user = UserModel(**args)
        db.session.add(user)
        db.session.commit()

        return {
            'code': Code.SUCCESS,
            'id': user.id,
            'uri': api.url_for(User, uid=user.id)
        }


class User(Resource):
    @Permissions.admin.require(403)
    @marshal_with(user_fields)
    def get(self, uid):
        return db.session.query(UserModel).filter_by(id=uid).first()

    @Permissions.admin.require(403)
    def post(self):
        abort(405)

    @Permissions.admin.require(403)
    def put(self, uid):
        args = get_parser().parse_args()

        set_data = {key: val for key, val in args.iteritems() if val is not None}
        print 'set_data', set_data

        db.session.query(UserModel).filter_by(id=uid).update(set_data)
        db.session.commit()
        return {'code': Code.SUCCESS}

    @Permissions.admin.require(403)
    def delete(self, uid):
        db.session.query(UserModel).filter_by(id=uid).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


def formatUser(user):
    groups = user.get_groups()
    perms = user.get_permissions()

    group_names = [group.name for group in groups]
    perm_tags = [p.tag for p in perms]

    _u = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'last_login': get_string_from_datetime(user.last_login),
        'date_joined': get_string_from_datetime(user.date_joined),
        'group_names': group_names,
        'permission_tags': perm_tags
    }

    return _u


class UserInfos(Resource):
    @Permissions.admin.require(403)
    def get(self):
        users = db.session.query(UserModel).all()

        ret = []
        for user in users:
            _u = formatUser(user)
            ret.append(_u)

        return ret


class UserInfo(Resource):
    def get(self, uid):
        print 'g.identity', g.identity
        if uid == 'now':
            uid = g.identity.auth_user.user.id

        user = db.session.query(UserModel).filter_by(id=uid).first()
        if not user:
            return {'code': Code.NOT_FOUND}

        ret = formatUser(user)

        return ret


api.add_resource(Users, '/', endpoint='.users')
api.add_resource(User, '/<string:uid>', endpoint='.user')
api.add_resource(UserInfos, '/infos/', endpoint='.user_infos')
api.add_resource(UserInfo, '/infos/<string:uid>', endpoint='.user_info')
