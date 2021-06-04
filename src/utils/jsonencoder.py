# -*- coding:utf-8 -*-
# Author:wu

from datetime import datetime, date

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
    解决datetime、date无法序列化的问题
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)
