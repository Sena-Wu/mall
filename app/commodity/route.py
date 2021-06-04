# -*- coding:utf-8 -*-
# Author:wu

from . import commodity


@commodity.route('/com')
def hello_world():
    return 'commodityyyyyyyy'
