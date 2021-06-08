# -*- coding:utf-8 -*-
# Author:wu
import random
from datetime import datetime, date, timedelta


# 生成一个指定长度随机字符串
def random_str(length: int) -> str:
    if length:
        alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()0123456789'
        return ''.join(random.sample(alphabet, length))
    return ''


# 生成一个在start_year-end_year之间的随机日期
def random_datetime(start_year: int, end_year: int) -> date:
    if start_year <= end_year:
        start = datetime(start_year, 1, 1, 0, 0, 0)
        if end_year < datetime.today().year:
            end = datetime(end_year, 12, 31, 23, 59, 59)
        else:
            end = datetime.today()
        # end = (end_year < datetime.today().year)? datetime(end_year, 12, 31, 23, 59, 59) : datetime.today()

        delta = random.randint(0, (end - start).days + 1)
        step = timedelta(days=delta)

        return start + step
