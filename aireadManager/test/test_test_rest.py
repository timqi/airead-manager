import json
from flask.ext.testing import TestCase
from main import app
from nose.tools import assert_equal


__author__ = 'airead'


class Test_test_rest(TestCase):
    def create_app(self):
        return app

    def test_get(self):
        rv = self.client.get('test_rest/')
        assert_equal(rv.data, '"test get"\n')

    def test_post(self):
        rv = self.client.post('test_rest/')
        assert_equal(rv.data, '"test post"\n')

    def test_get_rid(self):
        rv = self.client.get('test_rest/1')
        assert_equal(rv.data, '"get 1"\n')

    def test_post_rid(self):
        rv = self.client.post('test_rest/2')
        info = json.loads(rv.data)
        assert_equal(info['status'], 405)

    def test_put(self):
        rv = self.client.post('test_rest/3?at=put')
        assert_equal(rv.data, '"put 3"\n')

    def test_delete(self):
        rv = self.client.post('test_rest/4?at=delete')
        assert_equal(rv.data, '"delete 4"\n')