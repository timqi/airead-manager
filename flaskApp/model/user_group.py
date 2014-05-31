# coding=utf-8
from model.db_declare import db

__author__ = 'airead'


#序号	列名	数据类型	长度	小数位	标识	主键	允许空	默认值	说明
#1	id	int	4	0	是	是	否
#2	user_id	int	4	0			否		用户外键
#3	group_id	int	4	0			否		组外键


class UserGroupModel(db.Model):
    __tablename__ = 'user_groups'

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)
