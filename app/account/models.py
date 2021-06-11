# -*- coding:utf-8 -*-
# Author:wu

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
    根据id获取账户
    :param account_id: 账户id
    :return: 账户信息
    """
    query = Account.query
    acc = query.filter(Account.id == account_id).with_entities(Account.id, Account.account_name).first()

    return {
        "id": acc.id,
        "account_name": acc.account_name
    }


def get_by_params(params: dict) -> list:
    """
    分页查询账户数据
    :param params: 查询参数
    :return: 分页列表
    """
    acc_list = []
    query = Account.query
    query = query.filter(Account.account_name.like('%{}%'.format(params['account_name'])))

    order_value = Account.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    account_list = query.order_by(order_by).offset(params['from']).limit(params['size']).all()

    for acc in account_list:
        acc_list.append({
            "id": acc.id,
            "account_name": acc.account_name
        })
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
    query = Account.query
    acc = query.get(params['id'])
    if acc:
        for attr, value in params.items():
            setattr(acc, attr, value)  # 动态更改Account属性值
        try:
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise UpdateError(e)

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
