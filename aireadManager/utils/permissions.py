from flask.ext.principal import Permission, RoleNeed

__author__ = 'airead'


RoleList = [
    'admin',
    'guest',
]


class Roles(object):
    admin = RoleNeed('admin')
    guest = RoleNeed('guest')


class Permissions(object):
    admin = Permission(Roles.admin)
    guest = Permission(Roles.guest)