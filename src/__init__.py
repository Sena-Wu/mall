# -*- coding:utf-8 -*-
# Author:wu
import os

from flask import Flask

from .utils.conf import read_yaml
from .utils.jsonencoder import CustomJSONEncoder
from .utils.result import Res


def create_app(env=None):
    from . import db, account, order, commodity
    app = Flask(__name__)

    # 读取配置文件
    pwd = os.getcwd()
    if not env:
        config_path = os.path.join(pwd, 'conf{}dev.yaml'.format(os.sep))
    else:
        config_path = os.path.join(pwd, 'conf{}{}.yaml'.format(os.sep, env))

    conf = read_yaml(config_path)
    app.config.update(conf)
    # 替换默认的json编码器
    app.json_encoder = CustomJSONEncoder

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
