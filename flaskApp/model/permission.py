# coding=utf-8
from model.db_declare import db

__author__ = 'airead'


#序号	列名	数据类型	长度	小数位	标识	主键	允许空	默认值	说明
#1	id	int	4	0	是	是	否
#2	name	nvarchar	50	0			否
#3	content_type_id	int	4	0			否
#4	codename	nvarchar	100	0			否


class PermissionModel(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(50), unique=True, nullable=False)
