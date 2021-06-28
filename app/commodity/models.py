# -*- coding:utf-8 -*-
# Author:wu
from datetime import datetime

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
                Commodity.price, Commodity.description, Commodity.available_stock).first()

    return {
        "id": comm.id,
        "price": comm.price,
        "description": comm.description,
        "available_stock": comm.available_stock
    }


def get_by_params(params: dict) -> list:
    """
    分页查询商品数据
    :param params: 查询参数
    :return: 分页列表
    """
    comm_list = []
    query = Commodity.query
    query = query.filter(Commodity.description.like('%{}%'.format(params['description'])))

    order_value = Commodity.__dict__.get(params['order_value'])
    order_by = getattr(order_value, params['order_type'])()

    commodity_list = query.order_by(order_by).offset(params['from']).limit(params['size']).all()

    for comm in commodity_list:
        comm_list.append({
            "id": comm.id,
            "price": comm.price,
            "description": comm.description,
            "available_stock": comm.available_stock
        })
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
    :param params: 预处理好的商品信息
    :return:
    """
    query = Commodity.query
    comm = query.get(params['id'])
    if comm:
        for attr, value in params.items():
            setattr(comm, attr, value)  # 动态更改Commodity属性值
            comm.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise UpdateError(e)

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
    comm = query.get(commodity_id)

    if comm:
        try:
            db.session.delete(comm)
            db.session.commit()  # 写数据库
        except Exception as e:
            db.session.rollback()
            raise DeleteError(e)
        return {
            "id": comm.id,
            "price": comm.price,
            "description": comm.description,
            "available_stock": comm.available_stock
        }
    return {}
