# -*- coding: utf-8 -*-
"""
@File    : send_request.py
@Time    : 2026/7/14 17:41
@Author  : @叶风磊
@Desc    : 发送请求的方法封装
"""
import pymysql
import requests
import allure
import logging

from config.config import *

@allure.step('2、发送HTTP请求')
def send_http_request(**request_data):
    logging.info(f'2.发送http请求，响应“{requests.request(**request_data).text}')
    return requests.request(**request_data)


def send_jdbc_request(sql,index=0,):
    sq = pymysql.Connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME,
        charset = 'utf8',
        port = DB_PORT
    )
    # 创建游标
    cur = sq.cursor()

    # 查询语句
    cur.execute(sql)
    result = cur.fetchone()
    # 关闭游标和桥
    cur.close()
    sq.close()
    # 断言
    return result[index]
