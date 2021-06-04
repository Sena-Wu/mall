# -*- coding:utf-8 -*-
# Author:wu

from flask import request, current_app

from . import account
from ..utils.result import Res


@account.route(rule='', methods=['GET'])
def get_account():
    a = 1 / 0
    data = {
        "url": request.full_path,
        "methods": request.method
    }
    return Res.success(data)


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
