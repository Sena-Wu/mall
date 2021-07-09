# -*- coding:utf-8 -*-
# Author:wu

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:971211@127.0.0.1:3306/mall?charset=utf8'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session_factor = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
