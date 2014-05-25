import os
from flask.blueprints import Blueprint
from flask.ext.restful import Api
from utils.restful import Resource

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = Api(blueprint)


class Users(Resource):
    def get(self):
        return {'test': 'user'}

api.add_resource(Users, '/')

