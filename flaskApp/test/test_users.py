from flask.ext.testing import TestCase
from nose.tools import assert_equal
import json

from main import app
from model import db
from model.user import User


__author__ = 'airead'


class TestConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'


class Test_users(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        test1 = User(username='test1', email='email1')
        test2 = User(username='test2', email='email2')
        db.session.add(test1)
        db.session.add(test2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        rv = self.client.get('users/?at=get')
        print rv.data

    def test_post(self):
        user = {
            'username': 'Airead Fan',
            'email': 'fgh1987168@gmail.com'
        }
        data = {
            'user': json.dumps(user)
        }
        rv = self.client.post('users/?at=post', data=data)
        print rv.data

    def test_put(self):
        rv = self.client.post('users/?at=put')
        assert_equal(rv.data, 'test put')

    def test_delete(self):
        rv = self.client.post('users/?at=delete')
        print rv.data