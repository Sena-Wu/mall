# -*- coding:utf-8 -*-
# Author:wu
from flask import Blueprint

commodity = Blueprint('commodity', __name__)

from . import route
