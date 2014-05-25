from flask import request

__author__ = 'airead'


def restful(get, post, put, delete):
    ret = 'unknown method', 400
    action = request.values['at']
    action = action.upper()
    if action == 'GET':
        ret = get()
    elif action == 'POST':
        ret = post()
    elif action == 'PUT':
        ret = put()
    elif action == 'DELETE':
        ret = delete()

    print 'restful: ', ret
    return ret