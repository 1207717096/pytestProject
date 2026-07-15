# -*- coding: utf-8 -*-
"""
@File    : extractor.py
@Time    : 2026/7/14 18:31
@Author  : @叶风磊
@Desc    : 数据提取工具封装：json提取 + 数据库提取
"""
import logging

import jsonpath
import allure
from utils.send_request import send_jdbc_request


def json_extractor(case,all,res):
    # json提取
    if case['jsonExData']:
        # 首先要把jsonExData的key，value拆开
        with allure.step('4、JSON提取'):
            for key, value in eval(case["jsonExData"]).items():
                token = jsonpath.jsonpath(res.json(), value)[0]
                all[key] = token

            logging.info(f'4.JSON提取，根据{case["jsonExData"]} 提取数据，此时全量变量all为：{all}')

def jdbc_extractor(case,all):
    # 数据库提取
    if case['sqlExData']:
        with allure.step('4、JDBC提取'):
            for key, value in eval(case["sqlExData"]).items():
                all[key] = send_jdbc_request(value)
            logging.info(f'4.SQL提取，根据{case["sqlExData"]} 提取数据，此时全量变量all为：{all}')