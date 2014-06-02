from flask.ext.login import LoginManager, UserMixin
from aireadManager.model import db
from aireadManager.model.user import UserModel

__author__ = 'airead'

login_manager = LoginManager()


class AuthUser(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.id


@login_manager.user_loader
def load_user(userid):
    uid = int(userid)
    user = db.session.query(UserModel).filter_by(id=uid).first()
    if not user:
        return None

    return AuthUser(user)