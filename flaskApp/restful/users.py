from restful import restful
from model import db
from model.user import User
from flask import request
import json

__author__ = 'airead'


def users_restful():
    return restful(users_get, users_post, users_put, users_delete)


def users_get():
    users = User.query.all()
    print users
    return 'get users ok'


def users_post():
    user_json_str = request.form['user']
    print user_json_str
    userObj = json.loads(user_json_str)
    user = User(username=userObj['username'], email=userObj['email'])
    db.session.add(user)
    db.session.commit()

    return 'add user'


def users_put():
    return 'modify user'


def users_delete():
    User.query.delete()
    db.session.commit()
    return 'delete users'