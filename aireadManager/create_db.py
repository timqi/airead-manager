# coding=utf-8
from datetime import datetime

from main import app
from main import db
from model.user import UserModel
from model.permission import PermissionModel


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
    user = UserModel(**admin)
    db.session.add(user)
    db.session.commit()


def permission_init():
    permissions = [
        {'name': u'管理员', 'tag': 'admin'},
        {'name': u'游客', 'tag': 'guest'},
    ]

    for p in permissions:
        _ = PermissionModel(**p)
        db.session.add(_)

    db.session.commit()


with app.app_context():
    db.create_all()

    admin_init()
    permission_init()