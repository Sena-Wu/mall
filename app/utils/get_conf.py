# -*- coding:utf-8 -*-
# Author:wu

import logging
import os

import yaml

logger = logging.getLogger("root")  # 创建日志实例


def get_log_config(config_name=None):
    """
    读取log配置
    :param config_name:-logging
    :return:
    """
    if not config_name:
        return read_yaml('log')
    return read_yaml(config_name)


def get_env_config(config_name=None):
    """
    读取配置信息
    :param config_name:运行模式 - dev - test - prod
    """
    if not config_name:
        return read_yaml('dev')
    return read_yaml(config_name)


def read_yaml(config_name):
    """
    读取配置文件
    :param config_name:配置文件名
    """
    pwd = os.getcwd()  # D:\Active\Projects_python\mall\
    config_path = os.path.join(pwd, 'conf{}{}.yaml'.format(os.sep, config_name))

    logger.info("read config:{}".format(config_path))
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f.read())
    except Exception as e:
        logger.error(e)
        raise ValueError('请输入正确的配置名称或配置文件路径')
