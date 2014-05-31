# coding=utf-8
from model.db_declare import db

__author__ = 'airead'

#1	id	int	4	0	是	是	否
#2	name	nvarchar	80	0			否		组名称


class GroupModel(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    #: 组名称
    name = db.Column(db.String(80), unique=True, nullable=False)

    users = db.relationship('UserGroupModel', backref='group')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.username