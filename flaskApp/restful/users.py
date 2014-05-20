from restful import restful

__author__ = 'airead'


def users_restful():
    return restful(users_get, users_post, users_put, users_delete)


def users_get():
    return 'get users'


def users_post():
    return 'add user'


def users_put():
    return 'modify user'


def users_delete():
    return 'delete users'