from flask.ext import restful
from flask import request
from werkzeug.wrappers import Response as ResponseBase
from flask.ext.restful.utils import unpack


__author__ = 'airead'


class Resource(restful.Resource):
    def dispatch_request(self, *args, **kwargs):
        # Airead custom method, e.g. ?at=put
        print request.args
        method_name = request.args.get('at', None)
        if method_name is None:
            method_name = request.method.lower()

        meth = getattr(self, method_name, None)

        # Taken from flask
        #noinspection PyUnresolvedReferences
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        for decorator in self.method_decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or {}

        #noinspection PyUnresolvedReferences
        for mediatype in self.mediatypes():
            if mediatype in representations:
                data, code, headers = unpack(resp)
                resp = representations[mediatype](data, code, headers)
                resp.headers['Content-Type'] = mediatype
                return resp

        return resp
