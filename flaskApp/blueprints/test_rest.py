from flask.blueprints import Blueprint
import os
from flask.ext import restful
from utils.restful import Resource
from flask import abort

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)
api = restful.Api(blueprint)


class TestRestfuls(Resource):
    def get(self):
        return 'test get'

    def post(self):
        return 'test post'


class TestRestful(Resource):
    def get(self, rid):
        return 'get %s' % rid

    def post(self, rid):  # just for [put, delete] method allow by post
        abort(405)

    def put(self, rid):
        return 'put %s' % rid

    def delete(self, rid):
        return 'delete %s' % rid


api.add_resource(TestRestfuls, '/')
api.add_resource(TestRestful, '/<string:rid>')


def put():
    return 'test put'


def delete():
    return 'test delete'