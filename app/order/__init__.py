# -*- coding:utf-8 -*-
# Author:wu

from flask import Blueprint

order = Blueprint('order', __name__, url_prefix='/order')

from . import route
