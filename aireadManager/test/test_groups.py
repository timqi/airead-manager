# coding=utf-8
from flask.ext.testing import TestCase
from nose.tools import assert_equal

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.group import GroupModel
from aireadManager.test.init_te_st_db import TestDBConfig
from aireadManager.utils.errors import Code
from aireadManager.utils.permissions import Roles
from aireadManager.utils.principal import role_set


__author__ = 'airead'

SuccessRet = {
    'code': Code.SUCCESS
}

AdminGroup = {
    'name': u'管理组',
}

GuestGroup = {
    'name': u'客人组',
}


class Test_Groups(TestCase):
    def create_app(self):
        app.config.from_object(TestDBConfig)
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
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.get('/groups/')
        adminGroup, guestGroup = rv.json
        assert_equal(adminGroup['name'], AdminGroup['name'])
        assert_equal(guestGroup['name'], GuestGroup['name'])

    def test_groups_post(self):
        data = {
            'name': '超级管理员',
        }

        rv = self.client.post('groups/?at=post', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('groups/?at=post', data=data)
        print rv.json
        assert_equal(rv.json['uri'], '/groups/3')

        groups = db.session.query(GroupModel).all()
        assert_equal(len(groups), 3)

    def test_group_put(self):
        data = {
            'name': '笨蛋管理员'
        }
        rv = self.client.post('groups/1?at=put', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('groups/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        group = db.session.query(GroupModel).filter_by(id=1).one()
        assert_equal(group.name, u'笨蛋管理员')

    def test_group_delete(self):
        rv = self.client.post('groups/1?at=delete')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('groups/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        groups = db.session.query(GroupModel).all()
        assert_equal(len(groups), 1)
        group = groups[0]
        assert_equal(group.name, GuestGroup['name'])

    def test_group_get(self):
        rv = self.client.get('/groups/1')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.get('/groups/1')
        assert_equal(rv.json['name'], AdminGroup['name'])
