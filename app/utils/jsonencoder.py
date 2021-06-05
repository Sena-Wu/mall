# -*- coding:utf-8 -*-
# Author:wu

import decimal
import uuid
from datetime import datetime, date

from flask.json import JSONEncoder
from werkzeug.routing import Rule


class CustomJSONEncoder(JSONEncoder):  # 视图会自动将dict转换为JSON，但当dict中存在一些不可序列化的对象时无法转换，报错
    """
    解决datetime、date、Decimal无法序列化导致报错的问题·
    """

    def default(self, obj):

        if isinstance(obj, datetime):
            # 格式化时间
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            # 格式化日期
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            # 格式化Decimal
            return float(obj)
        elif isinstance(obj, Rule):  # "url": request.url_rule
            # return repr(obj)  # "<Rule '/accounts/<account_id>' (HEAD, GET, OPTIONS) -> account.get_account>"
            return str(obj)  # "/accounts/<account_id>"
        elif isinstance(obj, uuid.UUID):
            # 格式化uuid
            return str(obj)
        elif isinstance(obj, bytes):
            # 格式化字节数据
            return obj.decode("utf-8")

        return JSONEncoder.default(self, obj)
