from flask.ext.testing import TestCase
from nose.tools import assert_equal

from main import app
from model import db
from model.user import UserModel
from utils.errors import Code


__author__ = 'airead'


SuccessRet = {
    'code': Code.SUCCESS
}


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'


class Test_Group(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.user1 = dict(username='test1', email='email1')
        self.user2 = dict(username='test2', email='email2')
        test1 = UserModel(**self.user1)
        test2 = UserModel(**self.user2)
        db.session.add(test1)
        db.session.add(test2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        excepted_users = [
            {
                'username': 'test1',
                'email': 'email1'
            },
            {
                'username': 'test2',
                'email': 'email2'
            }
        ]
        rv = self.client.get('/users/')
        assert_equal(rv.json, excepted_users)

    def test_post(self):
        data = {
            'username': 'Airead Fan',
            'email': 'fgh1987168@gmail.com'
        }

        rv = self.client.post('users/?at=post', data=data)
        assert_equal(rv.json, SuccessRet)

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 3)

    def test_put(self):
        data = {
            'username': 'Airead'
        }
        rv = self.client.post('users/email1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        user = db.session.query(UserModel).filter_by(email='email1').one()
        assert_equal(user.username, 'Airead')

    def test_delete(self):
        rv = self.client.post('users/email1?at=delete')
        assert_equal(rv.json, SuccessRet)

        users = db.session.query(UserModel).all()
        assert_equal(len(users), 1)
        user = users[0]
        assert_equal(user.username, self.user2['username'])

    def test_get_by_email(self):
        rv = self.client.get('/users/email1')
        assert_equal(rv.json, self.user1)
