# -*- coding:utf-8 -*-
# Author:wu
import logging
from datetime import datetime

from flask import request

from app.order import order
from app.order.models import get_by_id, get_by_params, add_by_params, update_by_params, delete_by_id, \
    pay_by_id
from app.utils.result import Res, ResponseMessage
from .models import Order

logger = logging.getLogger("root")  # 创建日志实例


@order.route(rule='/<int:order_id>', methods=['GET'])
def get_order(order_id):
    data = get_by_id(order_id)
    return Res.success(data=data)


@order.route(rule='/', methods=['GET'])
def list_order():
    req_data = request.args
    params = {
        "from": req_data.get('from', 0),
        "size": req_data.get('size', 10),
        "page": req_data.get('page', 1),
        "account_id": req_data.get('account_id', 0),
        "order_description": req_data.get('order_description', ''),
        "order_value": req_data.get('order_value', "create_time"),
        "order_type": req_data.get('order_type', "desc"),
    }

    data = get_by_params(params)
    return Res.success(data=data)


@order.route(rule='/', methods=['POST'])
def add_order():
    req_data = request.args
    params = {
        'commodity_id': req_data.get('commodity_id', 0),
        'account_id': req_data.get('account_id', 0),
        'number': req_data.get('number', 0),
        'order_amount': req_data.get('order_amount', 0),
        'addr': req_data.get('addr', 'unknown'),
        'order_status': 0,
        'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'payment_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'close_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data = add_by_params(params)
    return Res.success(data)


@order.route(rule='/', methods=['PUT'])
def update_order():
    req_data = request.args

    if not req_data.get('id', 0):
        return Res.fail(ResponseMessage.BAD_REQUEST)
    else:
        try:
            int(req_data.get('id'))
        except Exception as e:
            logger.error('{} id格式有误'.format(request.url))
            return Res.fail(ResponseMessage.BAD_REQUEST)

    params = {}
    for attr, value in req_data.items():
        if attr in Order.__dict__.keys() - ('close_time', 'create_time', 'payment_time', 'order_status'):
            params[attr] = value

    data = update_by_params(params)
    return Res.success(data)


@order.route(rule='/<int:order_id>', methods=['PUT'])
def pay_order(order_id):
    if not order_id:
        return Res.fail(ResponseMessage.BAD_REQUEST)

    data = pay_by_id(order_id)
    return Res.success(data)


@order.route(rule='/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    data = delete_by_id(order_id)
    return Res.success(data)
