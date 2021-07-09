# -*- coding:utf-8 -*-
# Author:wu
from datetime import datetime
from math import ceil

from .. import db
from ..utils.error_class import InsertError, UpdateError, DeleteError


class Account(db.Model):
    # 声明表名
    __tablename__ = 'account_tb'
    # 建立字段函数
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(200))
    head_url = db.Column(db.String(200))
    cell_phone = db.Column(db.String(200))
    addr = db.Column(db.String(200))
    sex = db.Column(db.String(200))
    birthday = db.Column(db.String(200))
    money = db.Column(db.DECIMAL())
    create_time = db.Column(db.DateTime())
    update_time = db.Column(db.DateTime())


def get_by_id(account_id: int) -> dict:
    """
    根据id获取用户
    :param account_id: 用户id
    :return: 用户信息
    """
    query = Account.query
    acc = query.filter(Account.id == account_id).with_entities(Account.id, Account.account_name).first()

    return {
        "id": acc.id,
        "account_name": acc.account_name
    }


def get_by_params(params: dict) -> dict:
    """
    分页查询用户数据
    :param params: 查询参数
    :return: 分页列表
    """

    acc_list = {
        'accounts': [],
        'page': 1,
        'size': 0,
        'total': 0
    }
    query = Account.query
    query = query.filter(Account.account_name.like('%{}%'.format(params['account_name'])))

    count = len(query.all())
    if not count:
        return acc_list

    acc_list['total'] = count
    last_page = ceil(count / params['size'])
    params['page'] = last_page if params['page'] > last_page else params['page']
    acc_list['page'] = params['page']

    order_value = Account.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    # todo 分页查询优化一下：覆盖索引 + 延迟关联（子查询）
    offset = params['from'] + (params['page'] - 1) * params['size']
    account_list = query.order_by(order_by).offset(offset).limit(params['size']).all()

    for acc in account_list:
        acc_list['accounts'].append({
            "id": acc.id,
            "account_name": acc.account_name
        })
    acc_list['size'] = len(account_list)
    return acc_list


def add_by_params(params: dict) -> dict:
    """
    添加用户
    :param params: 预处理好的新用户信息
    :return:
    """
    acc = Account(**params)
    try:
        db.session.add(acc)
        db.session.commit()  # 写数据库
    except Exception as e:
        raise InsertError(e)

    return {
        "id": acc.id,
        "account_name": acc.account_name
    }


def update_by_params(params: dict) -> dict:
    """
    更新用户信息
    :param params: 预处理好的用户信息
    :return:
    """
    id = params.pop('id')
    params['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # update = 'UPDATE account_tb SET '
    # where = ' WHERE account_tb.id = ' + id
    #
    # for item in params.items():
    #     params[item[0]] = '"' + item[1] + '"' if isinstance(item[1], str) else str(item[1])
    # condition = ' ,'.join([' = '.join(item) for item in params.items()])

    # sql = update + condition + where

    try:
        Account.query.filter(Account.id == id).update(params)
        # db.session.execute(sql)
        db.session.commit()  # 写数据库

    except Exception as e:
        db.session.rollback()
        raise UpdateError(e)

    acc = Account.query.get(id)
    if acc:
        return {
            "id": acc.id,
            "account_name": acc.account_name
        }
    return {}


def delete_by_id(account_id: int) -> dict:
    """
    通过id删除用户
    :param account_id: 用户id
    :return:
    """
    query = Account.query
    acc = query.get(account_id)

    if acc:
        try:
            db.session.delete(acc)
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise DeleteError(e)
        return {
            "id": acc.id,
            "account_name": acc.account_name
        }
    return {}


def delete_by_params(params: dict) -> dict:
    """
    通过用户名删除用户
    :param params: 包含用户名的request参数字典
    :return:
    """
    query = Account.query
    query = query.filter(Account.account_name == params['account_name'])
    acc = query.first()

    if acc:
        try:
            db.session.delete(acc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DeleteError(e)
        return {
            "id": acc.id,
            "account_name": acc.account_name
        }
    return {}
