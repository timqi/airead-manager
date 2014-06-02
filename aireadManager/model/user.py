# coding=utf-8
from db_declare import db

__author__ = 'airead'


#序号	列名	数据类型	长度	小数位	标识	主键	允许空	默认值	说明
#1	id	int	4	0	是	是	否
#2	username	nvarchar	30	0			否		用户名
#3	first_name	nvarchar	30	0			否		名字
#4	last_name	nvarchar	30	0			否		姓氏
#5	email	nvarchar	75	0			否		邮箱
#6	password	nvarchar	128	0			否		密码
#7	is_staff	bit	1	0			否		是否为职员(0表示否，1表示是)
#8	is_active	bit	1	0			否
#9	is_superuser	bit	1	0			否		是否为超级管理员
#10	last_login	datetime	8	3			否		上次登陆时间
#11	date_joined	datetime	8	3			否		注册日期


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    #: 用户名
    username = db.Column(db.String(30), unique=True, nullable=False)
    #: 名字
    first_name = db.Column(db.String(30), nullable=False)
    #: 姓氏
    last_name = db.Column(db.String(30), nullable=False)
    #: 邮箱
    email = db.Column(db.String(75), unique=True, nullable=False)
    #: 密码
    password = db.Column(db.String(128), nullable=False)
    #: 是否为职员(0表示否，1表示是)
    is_staff = db.Column(db.Boolean, nullable=False)
    #: active
    is_active = db.Column(db.Boolean, nullable=False)
    #: 是否为超级管理员
    is_superuser = db.Column(db.Boolean, nullable=False)
    #: 上次登陆时间
    last_login = db.Column(db.DateTime, nullable=False)
    #: 注册日期
    date_joined = db.Column(db.DateTime, nullable=False)

    groups = db.relationship('UserGroupModel', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def get_groups(self):
        groups = set()
        for assoc in self.groups:
            g = assoc.group
            groups.add(g)

        return groups

    def get_permissions(self):
        permissions = set()
        groups = self.get_groups()

        for group in groups:
            for assoc in group.permissions:
                p = assoc.permission
                permissions.add(p)

        return permissions