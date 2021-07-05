# mall

## 目录结构

```scheme
mall
|-- README.md 项目描述
|-- app 业务代码
|   |-- __init__.py 初始化配置app,配置logging
|   |-- account 账户模块
|   |   |-- __init__.py 注册蓝图
|   |   |-- models.py
|   |   `-- route.py #view代码，restful风格编写
|   |-- commodity 账户模块
|   |   |-- __init__.py 注册蓝图
|   |   `-- route.py #view代码，restful风格编写
|   |-- db.py 数据库配置
|   |-- order 订单模块
|   |   `-- __init__.py
|   `-- utils 工具类
|       |-- __init__.py
|       |-- error_class.py 自定义InsertError等
|       |-- generate_random.py 
|       |-- get_conf.py 获取配置文件信息
|       |-- jsonencoder.py 重新定义JSONENCODER
|       `-- result.py 响应类
|-- tests 测试模块 (暂无)
|   |-- __init__.py 
|   |-- conftest.py 暂无
|   |-- test_create_db_data.py 生成批量合成数据写入数据库
|   `-- test_setup.py 暂无
|-- app.py 启动文件
|-- conf 配置文件
|   |-- dev.yaml #dev环境配置
|   |-- log.yaml #logging配置
|   |-- prod.yaml #prod环境配置
|   `-- test.yaml #test环境配置
|-- doc  
|   |-- requirement.md 需求文档
|   |-- sqlalchemy.md #关于sqlalchemy操作的一些说明
|   `-- sql  #mysql表结构
|       |-- account_tb.sql #用户表
|       |-- commodity_tb.sql #商品表
|       `-- order_tb.sql #订单表
|-- logs 日志
|   |-- errors.log 错误日志
|   `-- info.log 普通日志
`-- requirements.txt 

```

## Web模块

### 请求返回格式说明(以用户模块为例)

1. server内部异常，如代码中出现a = 4/0导致报错等

   ```json
   {
       "code": -1,
       "data": "server error",
       "msg": "失败"
   }
   ```

2. 404 异常

   ```json
   {
       "code": -1,
       "data": 404,
       "msg": "失败"
   }
   ```

3. 关键参数缺失或格式错误，请求失败

   ```json
   {
       "code": -1,
       "data": "Bad Request",
       "msg": "失败"
   }
   ```
   
   
   
4. 请求并操作成功，返回被操作数据简要信息

   ```JSON
   {
       "code": 0,
       "data": {
           "account_name": "嘤嘤",
           "id": 2
       },
       "msg": "成功"
   }
   ```

5. 请求成功但数据库查无此人

   ```json
   {
       "code": 0,
       "data": {},
       "msg": "成功"
   }
   ```

6. 请求成功但数据库写入失败,data部分提示"insert error"或"update error"或"delete error"

   ```json
   {
       "code": -1,
       "data": "insert error",
       "msg": "失败"
   }
   ```

   

### restful

项目 api 采用 restful 风格

详细资料：

1. [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)

### 全局异常处理

采用全局异常处理的方式，而不用每次都使用 try + except。

```python
# 全局错误处理
@app.errorhandler(Exception)
def framework_error(e):
    logger.error(e)
    return Res.fail("server error")

# 处理404异常
@app.errorhandler(404)
def page_not_found(e):
    logger.error(e)
    return Res.fail(404)
```

### 配置

配置文件采用 yaml 格式，[YAML 入门教程](https://www.runoob.com/w3cnote/yaml-intro.html)

需要先引入依赖 PyYAML

```shell
pip install PyYAML
```

配置工具类 get_conf.py ：

```python
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
    读取env配置信息
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
```

#### app配置

1. 先导入配置工具类

   ```python
   from .utils.get_conf import get_env_config, get_log_config
   ```

2. 读取配置

   ```python
   # 读取配置文件
   env_conf = get_env_config()
   app.config.update(env_conf)
   ```

#### logging配置

1. 先导入配置工具类

   ```python
   from .utils.get_conf import get_env_config, get_log_config
   ```

2. 读取配置

   ```python
   # 日志配置
   log_conf = get_log_config()
   logging.config.dictConfig(log_conf)
   ```

### 日志

需要先配置logging，可见：<a href="#logging配置">logging配置</a> 

日志配置文件：

```yaml
version: 1
disable_existing_loggers: False
# 定义日志输出格式，可以有多种格式输出
formatters:
  simple:
    format: "%(asctime)s [%(name)s] [%(levelname)s] :%(levelno)s: %(message)s"
  error:
    format: "%(asctime)s [%(name)s] [%(levelname)s] :%(levelno)s: %(message)s"

# 定义不同的handler，输出不同等级的日志消息,不同的处理器（handler）可以将日志输出到不同的位置
#每个handler都可以设置自己的过滤器（filter）实现日志过滤，可以设置自己的格式器（formatter）实现同一条日志以不同的格式输出到不同的地方。
handlers:
  console:
    class: logging.StreamHandler # 输出到控制台
    level: INFO
    formatter: simple
    stream: ext://flask.logging.wsgi_errors_stream # 监听flask日志
  info_file_handler:
    class: logging.handlers.RotatingFileHandler # 输出到文件
    level: INFO
    formatter: simple
    filename: ./logs/info.log
    maxBytes: 10485760 # 10MB
    backupCount: 20 #most 20 extensions
    encoding: utf8
  error_file_handler:
    class: logging.handlers.RotatingFileHandler # 输出到文件
    level: ERROR
    formatter: error
    filename: ./logs/errors.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8

#日志器，接管handler
root:
  level: INFO #日志器的级别，低于此级别的日志不处理
  handlers: [console,info_file_handler,error_file_handler]
```

使用时：

```python
logger = logging.getLogger('root') #指定日志器

logger.info("this is info")
logger.debug("this is debug")
logger.error("this is error")
```

注意日志的级别：**DEBUG < INFO < WARNING < ERROR < CRITICAL**

更多资料：

1. [Python之日志处理（logging模块） - 云游道士 - 博客园](https://www.cnblogs.com/yyds/p/6901864.html)
2. [python之配置日志的几种方式 - 云游道士 - 博客园](https://www.cnblogs.com/yyds/p/6885182.html)

### json序列化

视图会自动将dict转换为JSON，但当dict中存在一些不可序列化的对象时无法转换，会报错。

例如：datetime、date、Decimal

1. 自定义json编码器

   ```python
   import decimal
   import uuid
   from datetime import datetime, date
   
   from flask.json import JSONEncoder
   from werkzeug.routing import Rule
   
   
   class CustomJSONEncoder(JSONEncoder): 
       """
       解决datetime、date、Decimal无法序列化导致报错的问题·
       """
   
       def default(self, obj):
   
           if isinstance(obj, datetime):
               # 格式化时间
               return obj.strftime('%Y-%m-%d %H:%M:%S')
           elif isinstance(obj, date):
               # 格式化日期
               return obj.strftime('%Y-%m-%d')
           elif isinstance(obj, decimal.Decimal):
               # 格式化Decimal
               return float(obj)
           elif isinstance(obj, Rule):  # "url": request.url_rule
               # return repr(obj)  # "<Rule '/accounts/<account_id>' (HEAD, GET, OPTIONS) -> account.get_account>"
               return str(obj)  # "/accounts/<account_id>"
           elif isinstance(obj, uuid.UUID):
               # 格式化uuid
               return str(obj)
           elif isinstance(obj, bytes):
               # 格式化字节数据
               return obj.decode("utf-8")
   
           return JSONEncoder.default(self, obj)
   ```

2. 替换默认的json编码器

   ```python
   app.json_encoder = CustomJSONEncoder 
   ```

### 统一响应工具类

响应的数据格式如下：

- code：请求状态码，表示是否请求成功，0 表示成功，-1 表示失败
- data：请求时返回的数据
- msg：请求失败时的失败信息

例如：

```json
{
    "code": -1,
    "data": "server error",
    "msg": "失败"
}
```

统一响应工具类：

```python
class ResponseCode(object):
    SUCCESS = 0  # 成功
    FAIL = -1  # 失败


class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL = "失败"
    BAD_REQUEST = "Bad Request"


class Res(object):
    """
    封装统一响应工具类
    """

    @staticmethod
    def response(data, code, msg):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def success(data=None, code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS):
        return Res.response(data, code, msg)

    @staticmethod
    def fail(data=None, code=ResponseCode.FAIL, msg=ResponseMessage.FAIL):
        return Res.response(data, code, msg)
```

## 其他

### 导出requirements.txt

```shell
pip freeze > requirements.txt
```

### git 提交规范

提交格式：type: 具体的信息

type 有如下几种情况：

- feat：新功能（feature）

- fix：修补bug

- docs：文档（documentation）

- style： 格式（不影响代码运行的变动）

- refactor：重构（即不是新增功能，也不是修改bug的代码变动）

- test：增加测试

- chore：构建过程或辅助工具的变动


### git 打印项目目录结构

```shell
#3级目录，忽略__pycache__、venv文件夹,输出到README.md
tree -L 3 -I "__pycache__|venv" > README.md
```

常用：

```shell
tree -L 3 -I "__pycache__|venv"
```

更多资料：

1. [git生成文件目录树及日志打印](https://www.it610.com/article/1297493793985077248.htm)

### 启动方式

 1. 直接app.run()方式

    1. 打开terminal，使用命令行运行(推荐)

    ```shell
    python app.py
    ```

    2. 打开terminal，使用命令行运行：

    ```shell
    set FLASK_APP=app.py
    set FLASK_ENV=development # 可选development、production
    flask run --host '127.0.0.1' --port 8080 --debug True
    ```

    3. 直接用 pycharm 启动(此方式可能出现代码自定义配置不生效，需在Edit Configurations中添加自定义配置)

 2. 运用manager = flask_script.Manager(app) 接管app后，打开terminal,使用命令行运行

     1. 启动服务

        ```shell
        python app.py runserver
        ```

     2. 查看可用命令及命令用法

        ```shell
        python app.py
        ```


​      