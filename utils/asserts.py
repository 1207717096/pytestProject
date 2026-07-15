# -*- coding: utf-8 -*-
"""
@File    : asserts.py
@Time    : 2026/7/14 18:18
@Author  : @叶风磊
@Desc    : 断言文件的封装：http封装+数据库断言
"""
from unittest import result

import jsonpath
from utils.send_request import *

@allure.step('3、HTTP响应断言')
def http_assert(case,res,index=0):

    if case['check']:
        result = jsonpath.jsonpath(res.json(), case['check'])[index]
        logging.info(f'3.http响应断言的内容是：实际结果（ {result} ）== 预期结果（ {case["expected"]}）')
        assert result == case["expected"]

    else:
        logging.info(f'3.http响应断言的内容是：预期结果（ {case["expected"]} ）in 实际结果（ {res.text}）')
        assert case["expected"] in res.text

def jdbc_assert(case):
    # 数据库断言
    if case['sql_check'] and case['sql_expected']:
        # 链接数据库
        with allure.step('3.JDBC响应断言'):
            result = send_jdbc_request(case['sql_check'])
            logging.info(f'3.jdbc响应断言的内容：实际结果（ {result} ）== 预期结果（ {case["sql_expected"]}）')
            assert result == case['sql_expected']

