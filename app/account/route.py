# -*- coding:utf-8 -*-
# Author:wu

import logging
from datetime import datetime, date

from flask import request

from app.account import account
from app.account.models import get_by_id, get_by_params, add_by_params, update_by_params, delete_by_id, delete_by_params
from app.utils.generate_random import random_str
from app.utils.result import Res, ResponseMessage
from .models import Account

logger = logging.getLogger("root")  # 创建日志实例


@account.route(rule='/<int:account_id>', methods=['GET'])
def get_account(account_id: int):

    data = get_by_id(account_id)
    return Res.success(data=data)


@account.route(rule='/', methods=['GET'])
def list_account():
    req_data = request.args
    params = {
        "from": req_data.get('from', 0, type=int),
        "size": req_data.get('size', 10, type=int),
        "page": req_data.get('page', 1, type=int),
        "account_name": req_data.get('account_name', ''),
        "earlist": req_data.get('earlist', '2021-06-06 15:10:44'),
        "lastest": req_data.get('lastest', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "order_value": req_data.get('order_value', "create_time"),
        "order_type": req_data.get('order_type', "desc"),
    }

    data = get_by_params(params)
    return Res.success(data=data)


@account.route(rule='/', methods=['POST'])
def add_account():
    account_name = random_str(10)
    req_data = request.form
    params = {
        'account_name': req_data.get('account_name', account_name),
        'addr': req_data.get('addr', 'unknown'),
        'cell_phone': req_data.get('cell_phone', 'unknown'),
        'head_url': req_data.get('head_url', 'default.jpg'),
        'sex': req_data.get('sex', 0, type=int),
        'birthday': req_data.get('birthday', date.today()),
        'money': req_data.get('money', '0'),
        'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data = add_by_params(params)
    return Res.success(data)


@account.route(rule='/', methods=['PUT'])
def update_account():
    req_data = request.form

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
        if attr in Account.__dict__.keys() - ('create_time', 'update_time'):
            params[attr] = value

    data = update_by_params(params)
    return Res.success(data)


@account.route(rule='/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):

    data = delete_by_id(account_id)
    return Res.success(data)


@account.route(rule='/', methods=['DELETE'])
def delete_account_by_params():
    req_data = request.args
    if not req_data.get('account_name', 0):
        return Res.fail(ResponseMessage.BAD_REQUEST)

    data = delete_by_params(req_data)
    return Res.success(data)
