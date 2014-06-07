# coding=utf-8
import os
import json
from flask import request, redirect, current_app, g
from flask.blueprints import Blueprint
from flask.ext.restful import reqparse
from flask.ext.login import login_user
from flask.ext.principal import identity_changed, Identity
from aireadManager.model.user import UserModel
from aireadManager.model import db
from aireadManager.utils.errors import Code
from aireadManager.utils.login import AuthUser

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
blueprint = Blueprint(path, __name__, url_prefix='/' + path)


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    print request.method, request.form
    if request.method == 'GET':
        return redirect('static/login.html')

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    args = parser.parse_args()

    print 'login args:', args

    user = db.session.query(UserModel).filter_by(
        username=args['username']
    ).filter_by(password=args['password']).first()
    if not user:
        ret = {
            'code': Code.AUTH_FAILED,
            'flash': '帐号密码错误，请重新登陆'
        }
        return json.dumps(ret)

    print '用户登陆成功，', user

    auth_user = AuthUser(user)
    login_user(auth_user)

    identity_changed.send(current_app._get_current_object(), identity=Identity(auth_user.user.id))

    ret = {
        'code': Code.SUCCESS,
        'flash': '登陆成功'
    }
    return json.dumps(ret)


@blueprint.route('/cur_user')
def cur_user():
    print 'cur_user user: ', g.identity.auth_user.user.id
    print 'cur_user provides', g.identity.provides
    return g.identity.auth_user.user.username