# -*- coding:utf-8 -*-
# Author:wu
from flask import Blueprint

commodity = Blueprint('commodity', __name__, url_prefix='/commodity')

from . import route
