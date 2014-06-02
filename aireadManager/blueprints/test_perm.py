# coding=utf-8
import json
import os
from flask import Blueprint
from aireadManager.utils.errors import Code
from aireadManager.utils.permissions import Permissions


__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)


@blueprint.route('/test_admin')
@Permissions.admin.require(403)
def test_admin():
    ret = {
        'code': Code.SUCCESS,
        'desc': '你拥有 admin 权限'
    }

    return json.dumps(ret)


@blueprint.route('/test_guest')
def test_guest():
    ret = {
        'code': Code.SUCCESS,
        'desc': '你拥有 guest 权限'
    }

    return json.dumps(ret)
