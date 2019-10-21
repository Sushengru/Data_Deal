"""
    目的： 封装连接数据库的方法

"""

import pymysql
from sqlalchemy import create_engine

# BI brand 数据库配置
config_bi_brand = {
    'host': '192.168.12.182',
    'port': 3306,
    'user': 'yifan',
    'password': 'yifan',
    'db': 'brand',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

config_brand_pymysql = {
    'host': '192.168.15.138',
    'port': 3306,
    'user': 'yifan',
    'password': 'yifan',
    'db': 'brand',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# 服务器数据库
def db_brand_pymysql():
    conn_local = pymysql.connect(**config_brand_pymysql)
    return conn_local


def db_brand():
    connstr = 'mysql+pymysql://yifan:yifan@192.168.15.138/brand?charset=utf8'
    engine = create_engine(connstr, echo=True)
    return engine


# 封装用pymysql进行数据查询
def query_sql(db_connect, sql):
    try:
        with db_connect.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
    finally:
        pass
    return result


# 封装查询操作，commit查询操作，不返回result
def query_operation(db_connect, sql):
    try:
        with db_connect.cursor() as cur:
            cur.execute(sql)
            print(sql)
            db_connect.commit()
            print('commit complete')
    finally:
        pass
