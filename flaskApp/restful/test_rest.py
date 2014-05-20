from restful import restful

__author__ = 'airead'


def test_rest_restful():
    return restful(get, post, put, delete)


def get():
    return 'test get'


def post():
    return 'test post'


def put():
    return 'test put'


def delete():
    return 'test delete'