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

    return {
        "id": order.id,
        "order_status": order.order_status,
        "account_id": order.account_id
    }


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
    count = len(query.all())
    if not count:
        return order_list

    order_list['total'] = count
    last_page = ceil(count / params['size'])
    params['page'] = last_page if params['page'] > last_page else params['page']
    order_list['page'] = params['page']

    order_value = Order.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    offset = params['from'] + (params['page'] - 1) * params['size']
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
        "account_id": order.account_id
    }


def update_by_params(params: dict) -> dict:
    """
    更新订单信息
    :param params: 预处理好的订单信息
    :return:
    """
    id = params.pop('id')
    params['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # update = 'UPDATE order_tb SET '
    # where = ' WHERE order_tb.id = ' + id
    #
    # for item in params.items():
    #     params[item[0]] = '"' + item[1] + '"' if isinstance(item[1], str) else str(item[1])
    # condition = ' ,'.join([' = '.join(item) for item in params.items()])
    #
    # sql = update + condition + where

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


def pay_by_id(params: dict) -> dict:
    query = Order.query
    order = query.filter(Order.id == params[id]).with_for_update().first()

    # try:
    #     Order.query.filter(Order.id == id and order.order_status == 0).update(params)
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     raise UpdateError(e)
    if order:
        if order.order_status == 0:
            account_id = order.account_id
            account = Account.query.get(account_id)
            if account.money < order.order_amount:
                return {
                    "id": order.id,
                    "order_status": order.order_status,
                    "account_id": order.account_id,
                    "info": "money is not enough"
                }
            account.money -= order.order_amount
            order.payment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order.order_status = 1
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise UpdateError(e)
        return {
            "id": order.id,
            "order_status": order.order_status,
            "account_id": order.account_id,
            "info": "already pay"
        }
    return {}


def delete_by_id(order_id: int) -> dict:
    """
    通过id删除订单
    :param order_id: 订单id
    :return:
    """
    query = Order.query
    order = query.get(order_id)

    if order:
        try:
            order.close_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.delete(order)
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise DeleteError(e)
        return {
            "id": order.id,
            "order_status": order.order_status,
            "account_id": order.account_id
        }
    return {}
