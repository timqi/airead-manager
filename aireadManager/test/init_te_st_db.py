# coding=utf-8
from datetime import datetime

from aireadManager.model import db
from aireadManager.model.user import UserModel
from aireadManager.model.group import GroupModel
from aireadManager.model.user_group import UserGroupModel
from aireadManager.model.permission import PermissionModel
from aireadManager.model.group_permission import GroupPermissionModel


USER1 = {
    'username': 'user1',
    'first_name': 'us',
    'last_name': 'er1',
    'email': 'user1@a.com',
    'password': 'p1',
    'is_staff': True,
    'is_active': True,
    'is_superuser': True,
    'last_login': datetime.now(),
    'date_joined': datetime.now()
}

USER2 = {
    'username': 'user2',
    'first_name': 'us',
    'last_name': 'er2',
    'email': 'user2@a.com',
    'password': 'p2',
    'is_staff': False,
    'is_active': False,
    'is_superuser': False,
    'last_login': datetime.now(),
    'date_joined': datetime.now()
}

AdminGroup = {
    'name': u'管理组',
}

GuestGroup = {
    'name': u'客人组',
}

UserGroup1 = {
    'user_id': 1,
    'group_id': 2
}

UserGroup2 = {
    'user_id': 2,
    'group_id': 1
}

Perm1 = {
    'name': u'管理权限',
    'tag': 'admin'
}

Perm2 = {
    'name': u'客人权限',
    'tag': 'guest'
}

GroupPerm1 = {
    'group_id': 1,
    'permission_id': 2
}

GroupPerm2 = {
    'group_id': 2,
    'permission_id': 1
}


def user_init():
    u1 = UserModel(**USER1)
    u2 = UserModel(**USER2)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()


def group_init():
    g1 = GroupModel(**AdminGroup)
    g2 = GroupModel(**GuestGroup)
    db.session.add_all([g1, g2])
    db.session.commit()


def user_group_init():
    ug1 = UserGroupModel(**UserGroup1)
    ug2 = UserGroupModel(**UserGroup2)
    db.session.add_all([ug1, ug2])
    db.session.commit()


def permission_init():
    p1 = PermissionModel(**Perm1)
    p2 = PermissionModel(**Perm2)
    db.session.add_all([p1, p2])
    db.session.commit()


def group_permission_init():
    gp1 = GroupPermissionModel(**GroupPerm1)
    gp2 = GroupPermissionModel(**GroupPerm2)
    db.session.add_all([gp1, gp2])
    db.session.commit()


def init_db(used_app):
    with used_app.app_context():
        db.create_all()

        user_init()
        group_init()
        user_group_init()
        permission_init()
        group_permission_init()
