# -*- coding:utf-8 -*-
# Author:wu

import logging

from flask import request, current_app

from . import account
from ..utils.result import Res

logger = logging.getLogger("root")  # 创建日志实例


@account.route(rule='', methods=['GET'])
def get_account():
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


@account.route(rule='', methods=['PUT'])
def update_account():
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)


@account.route(rule='', methods=['DELETE'])
def delete_account():
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)
