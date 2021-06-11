# -*- coding:utf-8 -*-
# Author:wu

# db.create_all() 创建表，数据库中已经建好表的不需要
# db.drop_all() 删除表

# 在Flask-SQLAlchemy中，插入、修改、删除操作，均由数据库会话管理，查询操作是通过 query 对象操作数据

# SQLAlchemy查询，SQLAlchemy支持的Flask-SQLAlchemy都支持
# <模型类>.query.<过滤方法>.<查询方法>
# Account.query.filter(Account.id == 123).all()
# Account.query.all()