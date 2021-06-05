# -*- coding:utf-8 -*-
# Author:wu

import logging

from flask import request, current_app

from . import account
from ..utils.result import Res

logger = logging.getLogger("root")  # 创建日志实例


# 强制参数类型<int:account_id>;http://127.0.0.1:5000/accounts/123
@account.route(rule='/<int:account_id>', methods=['GET'])  # <int: account_id>ValueError: malformed url rule
def get_account(account_id: int):
    logger.info("account_id = " + str(account_id))
    data = {
        "url": request.url_rule,
        "methods": request.method
    }
    return Res.success(data=data)


# 请求格式http://127.0.0.1:5000/accounts/?xbox; http://127.0.0.1:5000/accounts/
@account.route(rule='/', methods=['GET'])
def list_account():
    logger.info("this is info")
    logger.debug("this is debug")
    logger.error("this is error")
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data=data)


@account.route(rule='', methods=['POST'])
def add_account():
    current_app.logger.info('111')
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)


@account.route(rule='/<account_id>', methods=['PUT'])
def update_account():
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)


@account.route(rule='/<account_id>', methods=['DELETE'])
def delete_account():
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)
