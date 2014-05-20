import os
from flask.blueprints import Blueprint
from restful.users import users_restful

__author__ = 'airead'


path = os.path.splitext(os.path.basename(__file__))[0]
url_prefix = '/' + path

blueprint = Blueprint(path, __name__, url_prefix='/' + path)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    ret = users_restful()
    return ret

