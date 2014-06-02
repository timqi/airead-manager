# coding=utf-8
from flask.ext.testing import TestCase
from nose.tools import assert_equal

from aireadManager.main import app
from aireadManager.model import db
from aireadManager.model.permission import PermissionModel
from aireadManager.utils.errors import Code


__author__ = 'airead'

SuccessRet = {
    'code': Code.SUCCESS
}

Perm1 = {
    'name': u'管理权限',
    'tag': 'admin'
}

Perm2 = {
    'name': u'客人权限',
    'tag': 'guest'
}


class TestConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test_manager.db'
    SQLALCHEMY_ECHO = False


class Test_Permissions(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        p1 = PermissionModel(**Perm1)
        p2 = PermissionModel(**Perm2)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_permissions_get(self):
        rv = self.client.get('/permissions/')
        adminGroup, guestGroup = rv.json
        assert_equal(adminGroup['name'], Perm1['name'])
        assert_equal(guestGroup['name'], Perm2['name'])

    def _test_permissions_post(self):
        data = {
            'name': '超级管理员',
            'tag': 'superAdmin',
        }

        rv = self.client.post('permissions/?at=post', data=data)
        print rv.json
        assert_equal(rv.json['uri'], '/permissions/3')

        permissions = db.session.query(PermissionModel).all()
        assert_equal(len(permissions), 3)

    def _test_permission_put(self):
        data = {
            'tag': 'stupidAdmin'
        }
        rv = self.client.post('permissions/1?at=put', data=data)
        assert_equal(rv.json, SuccessRet)

        group = db.session.query(PermissionModel).filter_by(id=1).one()
        assert_equal(group.tag, 'stupidAdmin')

    def _test_permission_delete(self):
        rv = self.client.post('permissions/1?at=delete')
        assert_equal(rv.json, SuccessRet)

        ps = db.session.query(PermissionModel).all()
        assert_equal(len(ps), 1)
        p = ps[0]
        assert_equal(p.name, Perm2['name'])

    def test_permission_get(self):
        rv = self.client.get('/permissions/1')
        assert_equal(rv.json['name'], Perm1['name'])
