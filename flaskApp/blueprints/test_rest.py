from flask.blueprints import Blueprint
import os
from restful.test_rest import test_rest_restful

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
url_prefix = '/' + path

blueprint = Blueprint(path, __name__, url_prefix='/' + path)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    ret = test_rest_restful()
    return ret