from flask.ext.testing import TestCase
from main import app
from nose.tools import assert_equal


__author__ = 'airead'


class Test_test_rest(TestCase):
    def create_app(self):
        return app

    def test_get(self):
        rv = self.client.get('test_rest/?at=get')
        assert_equal(rv.data, 'test get')

    def test_post(self):
        rv = self.client.post('test_rest/?at=post')
        assert_equal(rv.data, 'test post')

    def test_put(self):
        rv = self.client.post('test_rest/?at=put')
        assert_equal(rv.data, 'test put')

    def test_delete(self):
        rv = self.client.post('test_rest/?at=delete')
        assert_equal(rv.data, 'test delete')