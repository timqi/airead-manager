from main import app
from main import db
from model.user import UserModel

with app.app_context():
    db.create_all()

    user = UserModel('admin', 'admin')
    db.session.add(user)
    db.session.commit()