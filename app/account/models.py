# -*- coding:utf-8 -*-
# Author:wu

from datetime import datetime

from .. import db
from ..utils.error_class import Insert_Error


# noinspection SpellCheckingInspection
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


def get_by_id(account_id: int) -> list:
    """
    根据id获取账户
    :param account_id: 账户id
    :return: 账户信息
    """
    acc_list = []
    query = Account.query
    acc = query.filter(Account.id == account_id).with_entities(Account.id, Account.account_name).first()

    if acc:
        acc_list.append({
            "id": acc.id,
            "account_name": acc.account_name
        })
    return acc_list


def list_by_params(params: dict) -> list:
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


def add_by_params(params: dict) -> list:
    acc_list = []
    params['create_time'] = params['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    acc = Account(**params)

    db.session.add(acc)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Insert_Error(e)

    acc_list.append({
        "id": acc.id,
        "account_name": acc.account_name
    })
    return acc_list

def update_by_params(params: dict) -> list:
    pass
