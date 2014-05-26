import os
from flask import abort
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from utils.restful import Resource
from model.user import UserModel
from model import db
from utils.errors import Code

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)


user_fields = {
    'username': fields.String,
    'email': fields.String,
}


class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserModel.query.all()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        user = UserModel(args['username'], args['email'])
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


