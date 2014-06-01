from flask.ext.testing import TestCase
from nose.tools import assert_equal
from datetime import datetime

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.user import UserModel
from aireadManager.utils.errors import Code
from aireadManager.utils.util import get_string_from_datetime


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

    def test_users_get(self):
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
        assert_equal(rv.json['uri'], '/users/3')

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 3)

    def test_user_put(self):
        data = {
            'username': 'Airead'
        }
        rv = self.client.post('users/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        user = db.session.query(UserModel).filter_by(id=1).one()
        assert_equal(user.username, 'Airead')

    def test_user_delete(self):
        rv = self.client.post('users/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 1)
        user = users[0]
        assert_equal(user.username, USER2['username'])

    def test_user_get(self):
        rv = self.client.get('/users/1')
        user = rv.json
        assert_equal(user['username'], USER1['username'])
