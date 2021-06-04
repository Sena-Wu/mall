# -*- coding:utf-8 -*-
# Author:wu

import yaml


def read_yaml(config_path):
    """
    读取配置文件
    :param config_path:  配置文件
    """
    # todo 修改成日志打印
    print("read config:" + config_path)
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f.read())
    except Exception:
        raise ValueError('请输入正确的配置名称或配置文件路径')
