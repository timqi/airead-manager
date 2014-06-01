import os
from flask import abort, request, url_for
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.user import UserModel
from aireadManager.model import db
from aireadManager.utils.errors import Code
from aireadManager.utils.util import datetime_type

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


class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserModel.query.all()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('is_staff', type=bool, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        parser.add_argument('is_superuser', type=bool, required=True)
        parser.add_argument('last_login', type=datetime_type, required=True)
        parser.add_argument('date_joined', type=datetime_type, required=True)
        args = parser.parse_args()

        user = UserModel(**args)
        db.session.add(user)
        db.session.commit()

        return {'code': Code.SUCCESS, 'uri': api.url_for(User, uid=user.id)}


class User(Resource):
    @marshal_with(user_fields)
    def get(self, uid):
        return db.session.query(UserModel).filter_by(id=uid).first()

    def post(self):
        abort(405)

    def put(self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        set_data = {key: val for key, val in args.iteritems() if val is not None}

        db.session.query(UserModel).filter_by(id=uid).update(set_data)
        db.session.commit()
        return {'code': Code.SUCCESS}

    def delete(self, uid):
        db.session.query(UserModel).filter_by(id=uid).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


api.add_resource(Users, '/', endpoint='.users')
api.add_resource(User, '/<string:uid>', endpoint='.user')


