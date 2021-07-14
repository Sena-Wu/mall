# -*- coding:utf-8 -*-
# Author:wu
from datetime import datetime
from math import ceil

from .. import db
from ..account.models import Account
from ..utils.error_class import InsertError, UpdateError, DeleteError


class Order(db.Model):
    # 声明表名
    __tablename__ = 'order_tb'
    # 建立字段函数
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    account_id = db.Column(db.Integer)
    number = db.Column(db.Integer)  # 商品数量
    order_amount = db.Column(db.DECIMAL())  # 订单总金额
    addr = db.Column(db.String(200))
    order_status = db.Column(db.SmallInteger)  # （0：未支付，1：已支付，2：换货，3：退货）
    create_time = db.Column(db.DateTime())
    payment_time = db.Column(db.DateTime())
    close_time = db.Column(db.DateTime())


def get_by_id(order_id: int) -> dict:
    """
    根据id获取订单
    :param order_id: 订单id
    :return: 订单信息
    """
    query = Order.query
    order = query.filter(Order.id == order_id).with_entities(Order.id, Order.order_status, Order.account_id).first()

    if order:
        return {
            "id": order.id,
            "order_status": order.order_status,
            "account_id": order.account_id
        }
    return {}

def get_by_params(params: dict) -> list:
    """
    分页查询订单数据
    :param params: 查询参数
    :return: 分页列表
    """
    order_list = {
        'orders': [],
        'page': 1,
        'size': 0,
        'total': 0
    }
    query = Order.query
    #todo 增加查询条件
    query = query.filter()

    count = query.count()
    if not count:
        return order_list

    order_list['total'] = count
    last_page = ceil(count / params['size'])
    params['page'] = last_page if params['page'] > last_page else params['page']
    order_list['page'] = params['page']

    order_value = Order.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    offset = params['from'] + (params['page'] - 1) * params['size']
    subq = query.with_entities(Order.id).order_by(order_by).offset(offset).limit(params['size']).subquery()

    query = Order.query.join(
        subq, Order.id == subq.c.id
    )
    ord_list = query.order_by(order_by).offset(offset).limit(params['size']).all()

    for order in ord_list:
        order_list['orders'].append({
            "id": order.id,
            "order_status": order.order_status,
            "account_id": order.account_id
        })
    order_list['size'] = len(ord_list)
    return order_list


def add_by_params(params: dict) -> dict:
    """
    添加订单
    :param params: 预处理好的新订单信息
    :return:
    """
    order = Order(**params)
    try:
        db.session.add(order)
        db.session.commit()  # 写数据库
    except Exception as e:
        raise InsertError(e)

    return {
        "id": order.id,
        "order_status": order.order_status,
        "account_id": order.account_id,
        "order_amount": order.order_amount
    }


def update_by_params(params: dict) -> dict:
    """
    更新订单信息
    :param params: 预处理好的订单信息
    :return:
    """
    id = int(params.pop('id'))
    # update = 'UPDATE order_tb SET '
    # where = ' WHERE order_tb.id = ' + id
    #
    # for item in params.items():
    #     params[item[0]] = '"' + item[1] + '"' if isinstance(item[1], str) else str(item[1])
    # condition = ' ,'.join([' = '.join(item) for item in params.items()])
    #
    # sql = update + condition + where
    if params:
        try:
            Order.query.filter(Order.id == id).update(params)
            # db.session.execute(sql)
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise UpdateError(e)

    order = Order.query.get(id)
    if order:
        return {
            "id": order.id,
            "order_status": order.order_status,
            "account_id": order.account_id
        }
    return {}


def pay_by_id(order_id) -> dict:
    query = Order.query
    query = query.filter(Order.id == order_id, Order.order_status == 0)

    order = query.first()
    order_status = 0  # 订单修改标记
    pay_status = 0  # 账户修改标记

    if order:
        try:
            order_status = query.update(
                {'order_status': 1, 'payment_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            if order_status:
                pay_status = Account.query.filter(Account.id == order.account_id, Account.money >= order.order_amount).\
                    update({'money': Account.money - order.order_amount,
                            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        except Exception as e:
            db.session.rollback()
            raise UpdateError(e)

        if order_status and pay_status:
            db.session.commit()
            return {
                "id": order.id,
                "order_status": order.order_status,
                "account_id": order.account_id,
                "info": "already pay"
            }
        else:
            db.session.rollback()
        return {
                "id": order.id,
                "order_status": order.order_status,
                "account_id": order.account_id,
                "info": "支付失败"
        }
    return {}


def delete_by_id(order_id: int) -> dict:
    """
    通过id删除订单
    :param order_id: 订单id
    :return:
    """
    query = Order.query
    query = query.filter(Order.id == order_id)

    try:
        yes = query.delete()
        db.session.commit()  # 写数据库
    except Exception as e:
        db.session.rollback()
        raise DeleteError(e)
    return {
        "id": order_id,
        "info": '已删除'
    }
    return {}
