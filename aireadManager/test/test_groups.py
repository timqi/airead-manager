# coding=utf-8
from flask.ext.testing import TestCase
from nose.tools import assert_equal

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.group import GroupModel
from aireadManager.utils.errors import Code


__author__ = 'airead'

SuccessRet = {
    'code': Code.SUCCESS
}

AdminGroup = {
    'name': u'管理组',
    'tag': 'admin'
}

GuestGroup = {
    'name': u'客人组',
    'tag': 'guest'
}


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'
    SQLALCHEMY_ECHO = False


class Test_Groups(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        adminGroup = GroupModel(**AdminGroup)
        guestGroup = GroupModel(**GuestGroup)
        db.session.add(adminGroup)
        db.session.add(guestGroup)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_groups_get(self):
        rv = self.client.get('/groups/')
        adminGroup, guestGroup = rv.json
        assert_equal(adminGroup['tag'], AdminGroup['tag'])
        assert_equal(guestGroup['tag'], GuestGroup['tag'])

    def test_groups_post(self):
        data = {
            'name': '超级管理员',
            'tag': 'superAdmin'
        }

        rv = self.client.post('groups/?at=post', data=data)
        print rv.json
        assert_equal(rv.json['uri'], '/groups/3')

        groups = db.session.query(GroupModel).all()
        assert_equal(len(groups), 3)

    def test_group_put(self):
        data = {
            'tag': 'stupidAdmin'
        }
        rv = self.client.post('groups/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        group = db.session.query(GroupModel).filter_by(id=1).one()
        assert_equal(group.tag, 'stupidAdmin')

    def test_group_delete(self):
        rv = self.client.post('groups/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        groups = db.session.query(GroupModel).all()
        assert_equal(len(groups), 1)
        group = groups[0]
        assert_equal(group.name, GuestGroup['name'])

    def test_group_get(self):
        rv = self.client.get('/groups/1')
        assert_equal(rv.json['name'], AdminGroup['name'])
