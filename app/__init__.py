# -*- coding:utf-8 -*-
# Author:wu

import logging.config

from flask import Flask

from .utils.get_conf import get_env_config, get_log_config
from .utils.jsonencoder import CustomJSONEncoder
from .utils.result import Res


def create_app(env=None):
    from . import db, account, order, commodity
    app = Flask(__name__)

    # 日志设置
    log_conf = get_log_config()
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger('root')

    # 读取配置文件
    env_conf = get_env_config()
    app.config.update(env_conf)

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

    app.register_blueprint(account.account)
    app.register_blueprint(commodity.commodity)

    return app
