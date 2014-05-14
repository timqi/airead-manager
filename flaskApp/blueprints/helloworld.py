__author__ = 'airead'

from flask.blueprints import Blueprint

blueprint = Blueprint('helloworld', __name__, url_prefix='/helloworld')


@blueprint.route('/')
def index():
    return 'hello world'