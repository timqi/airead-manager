# coding=utf-8
from flask.ext.testing import TestCase
from nose.tools import assert_equal

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.group_permission import GroupPermissionModel
from aireadManager.utils.errors import Code


__author__ = 'airead'

SuccessRet = {
    'code': Code.SUCCESS
}

GroupPerm1 = {
    'group_id': 1,
    'permission_id': 2
}

GroupPerm2 = {
    'group_id': 2,
    'permission_id': 1
}


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'
    SQLALCHEMY_ECHO = False


class Test_GroupPermissions(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        group1 = GroupPermissionModel(**GroupPerm1)
        group2 = GroupPermissionModel(**GroupPerm2)
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_groups_get(self):
        rv = self.client.get('/group_permissions/')
        group1, group2 = rv.json
        assert_equal(group1['permission_id'], GroupPerm1['permission_id'])
        assert_equal(group1['group_id'], GroupPerm1['group_id'])
        assert_equal(group2['permission_id'], GroupPerm2['permission_id'])
        assert_equal(group2['group_id'], GroupPerm2['group_id'])

    def test_groups_post(self):
        data = {
            'group_id': 2,
            'permission_id': 2
        }

        rv = self.client.post('group_permissions/', data=data)
        assert_equal(rv.json['uri'], '/group_permissions/3')

        groups = db.session.query(GroupPermissionModel).all()
        assert_equal(len(groups), 3)

    def test_group_put(self):
        data = {
            'permission_id': 1
        }
        rv = self.client.post('group_permissions/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        group = db.session.query(GroupPermissionModel).filter_by(id=1).one()
        assert_equal(group.permission_id, 1)

    def test_group_delete(self):
        rv = self.client.post('group_permissions/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        groups = db.session.query(GroupPermissionModel).all()
        assert_equal(len(groups), 1)
        group = groups[0]
        assert_equal(group.permission_id, GroupPerm2['permission_id'])

    def test_group_get(self):
        rv = self.client.get('/group_permissions/1')
        assert_equal(rv.json['permission_id'], GroupPerm1['permission_id'])
        assert_equal(rv.json['group_id'], GroupPerm1['group_id'])
