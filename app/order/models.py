# -*- coding:utf-8 -*-
# Author:wu
from datetime import datetime

from .. import db
from ..utils.error_class import InsertError, UpdateError, DeleteError


class Order(db.Model):
    # 声明表名
    __tablename__ = 'order_tb'
    # 建立字段函数
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    account_id = db.Column(db.Integer)
    number = db.Column(db.Integer)  # 商品数量
    order_amount = db.Column(db.DECIMAL())
    addr = db.Column(db.String(200))
    order_status = db.Column(db.SmallInteger)
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
        "order_status": order.order_name,
        "account_id": order.account_id
    }


def get_by_params(params: dict) -> list:
    """
    分页查询订单数据
    :param params: 查询参数
    :return: 分页列表
    """
    order_list = []
    query = Order.query
    query = query.filter(Order.order_name.like('%{}%'.format(params['order_name'])))

    order_value = Order.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    order_list = query.order_by(order_by).offset(params['from']).limit(params['size']).all()

    for order in order_list:
        order_list.append({
            "id": order.id,
            "order_status": order.order_name,
            "account_id": order.account_id
        })
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
        "order_status": order.order_name,
        "account_id": order.account_id
    }


def update_by_params(params: dict) -> dict:
    """
    更新订单信息
    :param params: 预处理好的订单信息
    :return:
    """
    query = Order.query
    order = query.get(params['id'])
    if order:
        for attr, value in params.items():
            setattr(order, attr, value)  # 动态更改Order属性值
            order.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise UpdateError(e)

        return {
            "id": order.id,
            "order_status": order.order_name,
            "account_id": order.account_id
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
            db.session.delete(order)
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise DeleteError(e)
        return {
            "id": order.id,
            "order_status": order.order_name,
            "account_id": order.account_id
        }
    return {}
