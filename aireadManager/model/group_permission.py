# coding=utf-8
from db_declare import db

__author__ = 'airead'


#序号	列名	数据类型	长度	小数位	标识	主键	允许空	默认值	说明
#1	id	int	4	0	是	是	否
#2	group_id	int	4	0			否		组外键
#3	permission_id	int	4	0			否


class GroupPermissionModel(db.Model):
    __tablename__ = 'group_permissions'

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
