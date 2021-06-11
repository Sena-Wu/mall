# -*- coding:utf-8 -*-
# Author:wu
import random
from datetime import date, datetime

import pytest

from app.account.models import Account
from app.utils.generate_random import random_str, random_datetime
from . import db, app

total_account = 2000000
batch_size = 4000


def test_create_db_data():
    """
    生成数据
    """
    total_names = set()
    print('Start data generation....')
    for i in range(int(total_account / batch_size)):
        account_list = list()
        for _ in range(batch_size):
            length = random.randint(5, 15)
            account_name = random_str(length)
            while account_name in total_names:
                account_name = random_str(random.randint(5, 15))
            cities = ['unknown', '北京', '上海', '广州', '深圳', '成都', '南昌', '抚州', '泉州', '兰州', '长沙', '厦门', '西安']
            params = {
                'account_name': account_name,
                'addr': random.choice(cities),
                'cell_phone': 'unknown',
                'head_url': 'default.jpg',
                'sex': random.choice([0, 1, 2]),
                'birthday': random_datetime(1949, date.today().year),
                'money': random.choice(['0', ' 20', '50', '70', '100', '500', '1000', '4000', '9999']),
                'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            account_list.append(Account(**params))
        with app.app_context():
            try:
                db.session.add_all(account_list)
                db.session.commit()
            except Exception as e:
                print(str(e))
                db.session.rollback()
            print('{} epoch(s) finished!'.format(i))
    print('finished!')


if __name__ == '__main__':
    pytest.main(['-vs', 'test_create_db_data.py::test_create_db_data'])
