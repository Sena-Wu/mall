# -*- coding:utf-8 -*-
# Author:wu

# db.create_all() 创建表，数据库中已经建好表的不需要
# db.drop_all() 删除表

# 在Flask-SQLAlchemy中，插入、修改、删除操作，均由数据库会话管理，查询操作是通过 query 对象操作数据

# SQLAlchemy查询，SQLAlchemy支持的Flask-SQLAlchemy都支持
# <模型类>.query.<过滤方法>.<查询方法>
# Account.query.filter(Account.id == 123).all()
# Account.query.all()
from . import db

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    db.init_app(app)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
