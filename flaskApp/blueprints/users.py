from flask.blueprints import Blueprint
from restful import users

__author__ = 'airead'

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    ret = users.users_restful()
    return ret

