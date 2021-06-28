# -*- coding:utf-8 -*-
# Author:wu

import logging.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .utils.error_class import InsertError, UpdateError, DeleteError
from .utils.get_conf import get_env_config, get_log_config
from .utils.jsonencoder import CustomJSONEncoder
from .utils.result import Res

db = SQLAlchemy()
app = Flask(__name__)


def create_app():
    from . import account, order, commodity
    # 日志设置
    log_conf = get_log_config()
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger('root')

    # app配置
    env_conf = get_env_config()
    app.config.update(env_conf)

    # 数据库配置
    db.init_app(app=app)

    # 替换默认的json编码器
    app.json_encoder = CustomJSONEncoder

    # 处理404异常
    @app.errorhandler(404)
    def page_not_found(e):
        logger.error(e)
        return Res.fail(404)

    # 全局错误处理
    @app.errorhandler(Exception)
    def framework_error(e):
        logger.error(e)
        return Res.fail("server error")

    @app.errorhandler(InsertError)
    def insert_error(e):
        logger.error(e)
        return Res.fail("insert error")

    @app.errorhandler(UpdateError)
    def insert_error(e):
        logger.error(e)
        return Res.fail("update error")

    @app.errorhandler(DeleteError)
    def insert_error(e):
        logger.error(e)
        return Res.fail("delete error")

    app.register_blueprint(account.account)
    app.register_blueprint(commodity.commodity)
    app.register_blueprint(order.order)

    return app