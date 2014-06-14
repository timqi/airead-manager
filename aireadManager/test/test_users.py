from flask.ext.testing import TestCase
from nose.tools import assert_equal
from datetime import datetime

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.user import UserModel
from aireadManager.utils.errors import Code
from aireadManager.utils.util import get_string_from_datetime
from aireadManager.utils.principal import role_set
from aireadManager.utils.permissions import Roles
from aireadManager.test.init_te_st_db import USER1, USER2, init_db


__author__ = 'airead'

assert_equal.__self__.maxDiff = None

SuccessRet = {
    'code': Code.SUCCESS
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
        init_db(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users_get(self):
        rv = self.client.get('/users/')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.get('/users/')

        user1, user2 = rv.json
        assert_equal(user1['id'], 1)
        assert_equal(user1['username'], 'user1')
        assert_equal(user2['id'], 2)
        assert_equal(user2['username'], 'user2')

    def test_users_post(self):
        data = {
            'username': 'user3',
            'first_name': 'us',
            'last_name': 'er3',
            'email': 'user3@a.com',
            'password': 'p3',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
            'last_login': get_string_from_datetime(datetime.now()),
            'date_joined': get_string_from_datetime(datetime.now())
        }
        rv = self.client.post('users/?at=post', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('users/?at=post', data=data)
        assert_equal(rv.json['uri'], '/users/3')

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 3)

    def test_user_put(self):
        data = {
            'username': 'Airead'
        }
        rv = self.client.post('users/1?at=put', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('users/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        user = db.session.query(UserModel).filter_by(id=1).one()
        assert_equal(user.username, 'Airead')

    def test_user_delete(self):
        rv = self.client.post('users/1?at=delete')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('users/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 1)
        user = users[0]
        assert_equal(user.username, USER2['username'])

    def test_user_get(self):
        rv = self.client.get('/users/1')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.get('/users/1')
        user = rv.json
        assert_equal(user['username'], USER1['username'])

    def test_user_info_get(self):
        with role_set(Roles.admin):
            rv = self.client.get('/users/infos/1')
            print rv.data

    def test_cur_identity(self):
        with role_set(Roles.admin):
            rv = self.client.get('/login/cur_identity')
        print rv.data