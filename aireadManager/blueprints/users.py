import os
from flask import abort, request
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from aireadManager.utils.restful import Resource
from aireadManager.model.user import UserModel
from aireadManager.model import db
from aireadManager.utils.errors import Code
from aireadManager.utils.util import get_datetime_from_string

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
        print dict(request.form)
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('is_staff', type=bool, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        parser.add_argument('is_superuser', type=bool, required=True)
        parser.add_argument('last_login', type=get_datetime_from_string, required=True)
        parser.add_argument('date_joined', type=get_datetime_from_string, required=True)
        args = parser.parse_args()

        print 'args.last_login:', args['last_login']

        user = UserModel(args)
        db.session.add(user)
        db.session.commit()

        return {'code': Code.SUCCESS}


class User(Resource):
    @marshal_with(user_fields)
    def get(self, email):
        return db.session.query(UserModel).filter_by(email=email).first()

    def post(self):
        abort(405)

    def put(self, email):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        db.session.query(UserModel).filter_by(email=email).update(
            {UserModel.username: args['username']}
        )
        db.session.commit()
        return {'code': Code.SUCCESS}

    def delete(self, email):
        db.session.query(UserModel).filter_by(email=email).delete()
        db.session.commit()
        return {'code': Code.SUCCESS}


api.add_resource(Users, '/')
api.add_resource(User, '/<string:email>')


