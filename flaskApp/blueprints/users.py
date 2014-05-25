import os
from flask import abort
from flask.blueprints import Blueprint
from flask.ext.restful import Api, reqparse, fields, marshal_with
from utils.restful import Resource
from model.user import UserModel
from model import db

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


class User(Resource):
    @marshal_with(user_fields)
    def get(self, email):
        return db.session.query(UserModel).filter_by(email=email).first()


    def post(self):
        abort(405)

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(Users, '/')
api.add_resource(User, '/<string:email>')


