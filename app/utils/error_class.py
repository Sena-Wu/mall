# -*- coding:utf-8 -*-
# Author:wu

class InsertError(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        print(self.e)


class UpdateError(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        print(self.e)


class DeleteError(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        print(self.e)
