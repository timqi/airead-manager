__author__ = 'airead'

from flask.blueprints import Blueprint

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/')
def index():
    return 'users'