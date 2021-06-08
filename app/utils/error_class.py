# -*- coding:utf-8 -*-
# Author:wu

# todo 正确命名
class Insert_Error(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        print(self.e)

