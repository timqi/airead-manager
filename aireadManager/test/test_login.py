from flask.ext.testing import TestCase
from nose.tools import assert_equal
from datetime import datetime

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.user import UserModel
from aireadManager.utils.errors import Code


__author__ = 'airead'

assert_equal.__self__.maxDiff = None

SuccessRet = {
    'code': Code.SUCCESS
}

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


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'
    SQLALCHEMY_ECHO = False


class Test_users(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        test1 = UserModel(**USER1)
        test2 = UserModel(**USER2)
        db.session.add(test1)
        db.session.add(test2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        data = {
            'username': USER1['username'],
            'password': USER1['password']
        }
        rv = self.client.post('/login/', data=data)
        assert_equal(rv.json['code'], Code.SUCCESS)

    def test_login_failed(self):
        data = {
            'username': USER1['username'],
            'password': 'wrong password'
        }
        rv = self.client.post('/login/', data=data)
        assert_equal(rv.json['code'], Code.AUTH_FAILED)

    def test_login_principal_identity(self):
        data = {
            'username': USER1['username'],
            'password': USER1['password']
        }
        rv = self.client.post('/login/', data=data)
        assert_equal(rv.json['code'], Code.SUCCESS)

        rv = self.client.get('/login/cur_user')
        assert_equal(rv.data, USER1['username'])

    def test_login_user_permissions(self):
        db.drop_all()
        from aireadManager.create_db import init_db
        init_db(self.app)
        data = {
            'username': 'admin',
            'password': 'admin'
        }
        rv = self.client.post('/login/', data=data)
        assert_equal(rv.json['code'], Code.SUCCESS)