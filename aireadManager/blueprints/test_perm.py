# coding=utf-8
import json
import os
from flask import Blueprint
from aireadManager.utils.errors import Code
from aireadManager.utils.permissions import Permissions, RoleList


__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)


def gen_test_route(tag):
    """
    generated route is: /test_tag
    """

    route = '/test_' + tag

    perm = getattr(Permissions, tag)

    @blueprint.route(route, endpoint=route)
    @perm.require(403)
    def test():
        ret = {
            'code': Code.SUCCESS,
            'desc': '你拥有 %s 权限' % tag
        }

        return json.dumps(ret)


for role in RoleList:
    gen_test_route(role)