from flask.ext.principal import Permission, RoleNeed

__author__ = 'airead'


# used by ./utils/permissions.py
RoleList = [
    'admin',
    'guest',
    'databaseManager',
    'databaseSetting',
    'systemSetting',
    'holidayManager',
    'userManager',
    'groupManager'
]


class Roles(object):
    admin = RoleNeed('admin')
    guest = RoleNeed('guest')
    databaseManager = RoleNeed('databaseManager')
    databaseSetting = RoleNeed('databaseSetting')
    systemSetting = RoleNeed('systemSetting')
    holidayManager = RoleNeed('holidayManager')
    userManager = RoleNeed('userManager')
    groupManager = RoleNeed('groupManager')


class Permissions(object):
    admin = Permission(Roles.admin)
    guest = Permission(Roles.guest)
    databaseManager = Permission(Roles.databaseManager)
    databaseSetting = Permission(Roles.databaseSetting)
    systemSetting = Permission(Roles.systemSetting)
    holidayManager = Permission(Roles.holidayManager)
    userManager = Permission(Roles.userManager)
    groupManager = Permission(Roles.groupManager)