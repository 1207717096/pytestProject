from tempfile import template

import allure
import jsonpath
import pymysql
import pytest
import requests
from utils.allure_utils import allure_report_init
from jinja2 import Template
from openpyxl.styles.builtins import title
from pygments.lexers import data
from utils.excel_utils import read_excel
import logging
class TestRunner:
    #读测试数据
    data = read_excel()
    all = {}
    @pytest.mark.parametrize("case",data)
    def test_case(self,case):
        #引用全局变量（建立测试函数内外all，可以使用{}空字典）
        all = self.all
        case = eval(Template(str(case)).render(all))

        allure_report_init(case)

        #数据解析：1、url不存在；2、部分字符串的值变为字典；3、预期结果不能在请求中传输，会报错
        # 核心步骤1：解析请求参数
        method = case['method']
        url = 'http://127.0.0.1:8888/api/private/v1'+case['path']
        headers = eval(case['headers']) if isinstance(case['headers'], str) else None
        params = eval(case['params']) if isinstance(case['params'], str) else None
        data = eval(case["data"]) if isinstance(case["data"], str) else None
        json = eval(case['json']) if isinstance(case['json'], str) else None
        files = eval(case['files']) if isinstance(case['files'], str) else None

        request_data = {
            'method': method,
            'url': url,
            'headers': headers,
            'params': params,
            'data': data,
            'json': json,
            'files': files
        }

        # 核心步骤2：发起请求，得到响应结果
        res = requests.request(**request_data)

        # 核心步骤3：处理断言
        #HTTP响应断言
        # assert res.json()['meta']['msg'] == case['expected']
        if case['check']:
            assert jsonpath.jsonpath(res.json(),case['check'])[0] == case["expected"]

        else:
            assert case["expected"] in res.text

        #数据库断言
        if case['sql_check'] and case['sql_expected']:
            #链接数据库
            sq = pymysql.Connect(
                host = '127.0.0.1',
                user = 'root',
                password = '123456',
                database = 'mydb',
                charset = 'utf8',
                port = 3306
            )
            #创建游标
            cur = sq.cursor()

            #查询语句
            cur.execute(case['sql_check'])
            result = cur.fetchone()
            #关闭游标和桥
            cur.close()
            sq.close()
            #断言
            assert result[0] == case["sql_expected"]

            #json提取
            if case['jsonExData']:
                #首先要把jsonExData的key，value拆开
                for key,value in eval(case["jsonExData"]).items():
                    token = jsonpath.jsonpath(res.json(),value)[0]
                    all[key] = token
            #数据库提取
            if case['sqlExData']:
                for key,value in eval(case["sqlExData"]).items():
                    sq = pymysql.Connect(
                        host='127.0.0.1',
                        user='root',
                        password='123456',
                        database='mydb',
                        charset='utf8',
                        port=3306
                    )
                    # 创建游标
                    cur = sq.cursor()

                    # 查询语句
                    cur.execute(value)
                    result = cur.fetchone()
                    all[key] = result[0]
                    cur.close()
                    sq.close()