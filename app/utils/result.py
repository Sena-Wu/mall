# -*- coding:utf-8 -*-
# Author:wu


class ResponseCode(object):
    SUCCESS = 0  # 成功
    FAIL = -1  # 失败


class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL = "失败"


class Res(object):
    """
    封装统一响应工具类
    """

    @staticmethod
    def response(data, code, msg):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def success(data=None, code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS):
        Res.response(data, code, msg)

    @staticmethod
    def fail(data=None, code=ResponseCode.FAIL, msg=ResponseMessage.FAIL):
        Res.response(data, code, msg)
