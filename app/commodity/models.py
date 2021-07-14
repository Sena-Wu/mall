# -*- coding:utf-8 -*-
# Author:wu
from datetime import datetime
from math import ceil

from .. import db
from ..utils.error_class import InsertError, UpdateError, DeleteError


class Commodity(db.Model):
    # 声明表名
    __tablename__ = 'commodity_tb'
    # 建立字段函数
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.DECIMAL())
    description = db.Column(db.String(200))
    total_stock = db.Column(db.Integer)
    available_stock = db.Column(db.Integer)
    create_time = db.Column(db.DateTime())
    update_time = db.Column(db.DateTime())


def get_by_id(commodity_id: int) -> dict:
    """
    根据id获取商品
    :param commodity_id: 商品id
    :return: 商品信息
    """
    query = Commodity.query
    comm = query.filter(Commodity.id == commodity_id).with_entities(Commodity.id,
                                                                    Commodity.price, Commodity.description,
                                                                    Commodity.available_stock).first()
    if comm:
        return {
            "id": comm.id,
            "price": comm.price,
            "description": comm.description,
            "available_stock": comm.available_stock
        }
    return {}


def get_by_params(params: dict) -> list:
    """
    分页查询商品数据
    :param params: 查询参数
    :return: 分页列表
    """
    comm_list = {
        'commodities': [],
        'page': 1,
        'size': 0,
        'total': 0
    }
    query = Commodity.query
    query = query.filter(Commodity.description.like('%{}%'.format(params['description'])))
    query = query.filter(Commodity.price >= params['floor_price'], Commodity.price <= params['peak_price'])

    count = query.count()
    if not count:
        return comm_list

    comm_list['total'] = count
    last_page = ceil(count / params['size'])
    params['page'] = last_page if params['page'] > last_page else params['page']
    comm_list['page'] = params['page']

    order_value = Commodity.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    offset = params['from'] + (params['page'] - 1) * params['size']
    subq = query.with_entities(Commodity.id).order_by(order_by).offset(offset).limit(params['size']).subquery()

    query = Commodity.query.join(
        subq, Commodity.id == subq.c.id
    )
    commodity_list = query.all()

    for comm in commodity_list:
        comm_list['commodities'].append({
            "id": comm.id,
            "price": comm.price,
            "description": comm.description,
            "available_stock": comm.available_stock
        })
    comm_list['size'] = len(commodity_list)
    return comm_list


def add_by_params(params: dict) -> dict:
    """
    添加商品
    :param params: 预处理好的新商品信息
    :return:
    """
    comm = Commodity(**params)
    try:
        db.session.add(comm)
        db.session.commit()  # 写数据库
    except Exception as e:
        raise InsertError(e)

    return {
        "id": comm.id,
        "price": comm.price,
        "description": comm.description,
        "available_stock": comm.available_stock
    }


def update_by_params(params: dict) -> dict:
    """
    更新商品信息
    :param params: 预处理好的待更新商品信息
    :return:
    """
    id = int(params.pop('id'))
    params['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # update = 'UPDATE commodity_tb SET '
    # where = ' WHERE commodity_tb.id = ' + id
    #
    # for item in params.items():
    #     params[item[0]] = '"' + item[1] + '"' if isinstance(item[1], str) else str(item[1])
    # condition = ' ,'.join([' = '.join(item) for item in params.items()])
    #
    # sql = update + condition + where

    try:
        Commodity.query.filter(Commodity.id == id).update(params)
        # db.session.execute(sql)
        db.session.commit()  # 写数据库

    except Exception as e:
        db.session.rollback()
        raise UpdateError(e)

    comm = Commodity.query.get(id)

    if comm:
        return {
            "id": comm.id,
            "price": comm.price,
            "description": comm.description,
            "available_stock": comm.available_stock
        }
    return {}


def delete_by_id(commodity_id: int) -> dict:
    """
    通过id删除商品
    :param commodity_id: 商品id
    :return:
    """
    query = Commodity.query
    query = query.filter(Commodity.id == commodity_id)

    try:
        yes = query.delete()
        db.session.commit()  # 写数据库
    except Exception as e:
        db.session.rollback()
        raise DeleteError(e)
    if yes:
        return {
            "id": commodity_id,
            "info": '已删除'
        }
    return {}
