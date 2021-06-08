# -*- coding:utf-8 -*-
# Author:wu

import logging.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .utils.error_class import Insert_Error
from .utils.get_conf import get_env_config, get_log_config
from .utils.jsonencoder import CustomJSONEncoder
from .utils.result import Res


db = SQLAlchemy()  # 先创建，方便其他模块引入

def create_app():

    app = Flask(__name__)
    from . import account, order, commodity
    # 日志设置
    log_conf = get_log_config()
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger('root')

    # app配置
    env_conf = get_env_config()
    app.config.update(env_conf)

    # 数据库配置
    SQLAlchemy(app=app)

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

    @app.errorhandler(Insert_Error)
    def insert_error(e):
        logger.error(e)
        return Res.fail("insert error")

    app.register_blueprint(account.account)
    app.register_blueprint(commodity.commodity)

    return app
