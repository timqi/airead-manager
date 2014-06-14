# coding=utf-8
from flask.ext.testing import TestCase
from nose.tools import assert_equal

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.user_group import UserGroupModel
from aireadManager.test.init_te_st_db import TestDBConfig
from aireadManager.utils.errors import Code
from aireadManager.utils.permissions import Roles
from aireadManager.utils.principal import role_set


__author__ = 'airead'

SuccessRet = {
    'code': Code.SUCCESS
}

UserGroup1 = {
    'user_id': 1,
    'group_id': 2
}

UserGroup2 = {
    'user_id': 2,
    'group_id': 1
}


class Test_UserGroups(TestCase):
    def create_app(self):
        app.config.from_object(TestDBConfig)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        group1 = UserGroupModel(**UserGroup1)
        group2 = UserGroupModel(**UserGroup2)
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_groups_get(self):
        rv = self.client.get('/user_groups/')
        group1, group2 = rv.json
        assert_equal(group1['user_id'], UserGroup1['user_id'])
        assert_equal(group1['group_id'], UserGroup1['group_id'])
        assert_equal(group2['user_id'], UserGroup2['user_id'])
        assert_equal(group2['group_id'], UserGroup2['group_id'])

    def test_groups_post(self):
        data = {
            'user_id': 1,
            'group_id': 1
        }

        rv = self.client.post('user_groups/?at=post', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('user_groups/?at=post', data=data)
        assert_equal(rv.json['uri'], '/user_groups/3')

        groups = db.session.query(UserGroupModel).all()
        assert_equal(len(groups), 3)

    def test_group_put(self):
        data = {
            'group_id': 1
        }
        rv = self.client.post('user_groups/1?at=put', data=data)
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('user_groups/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        group = db.session.query(UserGroupModel).filter_by(id=1).one()
        assert_equal(group.group_id, 1)

    def test_group_delete(self):
        rv = self.client.post('user_groups/1?at=delete')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('user_groups/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        groups = db.session.query(UserGroupModel).all()
        assert_equal(len(groups), 1)
        group = groups[0]
        assert_equal(group.group_id, UserGroup2['group_id'])

    def test_group_get(self):
        rv = self.client.get('/user_groups/1')
        assert_equal(rv.json['user_id'], UserGroup1['user_id'])
        assert_equal(rv.json['group_id'], UserGroup1['group_id'])

    def test_group_delete_by_user_group_id(self):
        rv = self.client.post('/user_groups/1/2?at=delete')
        self.assert403(rv)

        with role_set(Roles.admin):
            rv = self.client.post('/user_groups/1/2?at=delete')
        assert_equal(rv.json, SuccessRet)

        groups = db.session.query(UserGroupModel).all()
        assert_equal(len(groups), 1)
        group = groups[0]
        assert_equal(group.group_id, UserGroup2['group_id'])
