# -*- coding:utf-8 -*-
# Author:wu

import logging
import random

from flask import request

from app.account import account
from app.account.models import get_by_id, list_by_params, add_by_params, update_by_params
from app.utils.result import Res
from app.utils.generate_random import random_str
from datetime import datetime, date

logger = logging.getLogger("root")  # 创建日志实例


@account.route(rule='/<int:account_id>', methods=['GET'])
def get_account(account_id: int):
    data = get_by_id(account_id)
    return Res.success(data=data)


@account.route(rule='/', methods=['GET'])
def list_account():
    req_data = request.args
    params = {
        "from": req_data.get('from', 0),
        "size": req_data.get('size', 10),
        "account_name": req_data.get('account_name', ''),
        "order_value": req_data.get('order_value', "create_time"),
        "order_type": req_data.get('order_type', "desc"),
    }

    data = list_by_params(params)
    return Res.success(data=data)


@account.route(rule='/', methods=['POST'])
def add_account():
    account_name = random_str(10)
    # account_name = ''
    req_data = request.args
    params = {
        'account_name': req_data.get('account_name', account_name),
        'addr': req_data.get('addr', 'unknown'),
        'cell_phone': req_data.get('cell_phone', 'unknown'),
        'head_url': req_data.get('head_url', 'default.jpg'),
        'sex': req_data.get('sex', 0),
        'birthday': req_data.get('birthday', date.today()),
        'money': req_data.get('money', '0'),
        'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data = add_by_params(params)
    return Res.success(data)


@account.route(rule='/', methods=['PUT'])
def update_account():
    req_data = request.args
    if req_data['id'] or req_data['account_name']:
        params = req_data
        data = update_by_params(params)

    return Res.success(data)


@account.route(rule='/<account_id>', methods=['DELETE'])
def delete_account():
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)
