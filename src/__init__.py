# -*- coding:utf-8 -*-
# Author:wu

from flask import Flask

from .utils.jsonencoder import CustomJSONEncoder
from .utils.result import Res


def create_app():
    from . import db, account, order, commodity
    app = Flask(__name__)

    # 替换默认的json编码器
    app.json_encoder = CustomJSONEncoder

    # 修改app配置
    app.config['ENV'] = 'development'

    # app.config.update(ENV='development', SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/')

    # 处理404异常
    @app.errorhandler(404)
    def page_not_found(e):
        # todo 打印日志
        return Res.fail(404)

    # 全局错误处理
    @app.errorhandler(Exception)
    def framework_error(e):
        # todo 打印日志
        return Res.fail("server error")

    app.register_blueprint(account.account)
    app.register_blueprint(commodity.commodity)
    return app
