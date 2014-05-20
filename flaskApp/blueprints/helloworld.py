import os
from flask.blueprints import Blueprint

__author__ = 'airead'

path = os.path.splitext(os.path.basename(__file__))[0]
url_prefix = '/' + path

blueprint = Blueprint(path, __name__, url_prefix='/' + path)


@blueprint.route('/')
def index():
    return 'hello world'