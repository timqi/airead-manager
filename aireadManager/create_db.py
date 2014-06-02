# coding=utf-8
from datetime import datetime

from main import app
from main import db
from aireadManager.model.user import UserModel
from aireadManager.model.group import GroupModel
from aireadManager.model.user_group import UserGroupModel
from aireadManager.model.permission import PermissionModel
from aireadManager.model.group_permission import GroupPermissionModel


def admin_init():
    admin = {
        'username': 'admin',
        'first_name': 'admin',
        'last_name': 'admin',
        'email': 'admin@some.com',
        'password': 'admin',
        'is_staff': True,
        'is_active': True,
        'is_superuser': True,
        'last_login': datetime.now(),
        'date_joined': datetime.now()
    }

    u = db.session.query(UserModel).filter_by(username='admin').first()
    if u:
        return None

    user = UserModel(**admin)
    db.session.add(user)
    db.session.commit()


def group_init():
    group = {
        'name': u'管理组'
    }

    existed = db.session.query(GroupModel).filter_by(name=group['name']).first()
    if not existed:
        g = GroupModel(**group)
        db.session.add(g)
        db.session.commit()


def user_group_init():
    adminUser = db.session.query(UserModel).filter_by(username='admin').first()
    if not adminUser:
        raise Exception('没有发现管理员用户')

    adminGroup = db.session.query(GroupModel).filter_by(name=u'管理组').first()
    if not adminGroup:
        raise Exception('没有发现管理组')

    adminUserGroup = db.session.query(UserGroupModel).filter_by(
        user_id=adminUser.id
    ).filter_by(
        group_id=adminGroup.id
    ).first()
    if not adminUserGroup:
        u_g = UserGroupModel(user_id=adminUser.id, group_id=adminGroup.id)
        db.session.add(u_g)
        db.session.commit()


def permission_init():
    permissions = [
        {'name': u'管理员', 'tag': 'admin'},
        {'name': u'游客', 'tag': 'guest'},
    ]

    for p in permissions:
        existed = db.session.query(PermissionModel).filter_by(tag=p['tag']).first()
        if existed:
            continue
        _ = PermissionModel(**p)
        db.session.add(_)

    db.session.commit()


def group_permission_init():
    adminGroup = db.session.query(GroupModel).filter_by(name=u'管理组').first()
    if not adminGroup:
        raise Exception('没有发现管理组')

    adminPerm = db.session.query(PermissionModel).filter_by(tag='admin').first()
    if not adminPerm:
        raise Exception('没有发现管理权限')

    adminGroupPerm = db.session.query(GroupPermissionModel).filter_by(
        group_id=adminGroup.id
    ).filter_by(
        permission_id=adminPerm.id
    ).first()
    if not adminGroupPerm:
        g_p = GroupPermissionModel(group_id=adminGroup.id, permission_id=adminPerm.id)
        db.session.add(g_p)
        db.session.commit()


with app.app_context():
    db.create_all()

    admin_init()
    group_init()
    user_group_init()
    permission_init()
    group_permission_init()
