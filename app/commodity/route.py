# -*- coding:utf-8 -*-
# Author:wu

from datetime import datetime

from flask import request

from app.commodity import commodity
from app.commodity.models import get_by_id, get_by_params, add_by_params, update_by_params, delete_by_id
from app.utils.result import Res, ResponseMessage
from .models import Commodity


@commodity.route(rule='/<int:commodity_id>', methods=['GET'])
def get_commodity(commodity_id):

    data = get_by_id(commodity_id)
    return Res.success(data=data)


@commodity.route(rule='/', methods=['GET'])
def list_commodity():
    req_data = request.args
    params = {
        "from": req_data.get('from', 0),
        "size": req_data.get('size', 10),
        "description": req_data.get('description', ''),
        "order_value": req_data.get('order_value', "create_time"),
        "order_type": req_data.get('order_type', "desc"),
    }

    data = get_by_params(params)
    return Res.success(data=data)


@commodity.route(rule='/', methods=['POST'])
def add_commodity():
    price = 999999999999.99
    req_data = request.args
    params = {
        'price': req_data.get('price', price),
        'description': req_data.get('description', 'unknown'),
        'total_stock': req_data.get('total_stock', 0),
        'available_stock': req_data.get('available_stock', req_data.get('total_stock', 0)),
        'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data = add_by_params(params)
    return Res.success(data)


@commodity.route(rule='/', methods=['PUT'])
def update_commodity():
    req_data = request.args

    if not req_data.get('id', 0):
        return Res.fail(ResponseMessage.BAD_REQUEST)
    params = {}
    for attr, value in req_data.items():
        if attr in Commodity.__dict__.keys():
            params[attr] = value

    data = update_by_params(params)
    return Res.success(data)


@commodity.route(rule='/<int:commodity_id>', methods=['DELETE'])
def delete_commodity(commodity_id):
    data = delete_by_id(commodity_id)
    return Res.success(data)
