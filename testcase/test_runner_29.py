from unittest import case

import jsonpath
import pytest
import requests
from pygments.lexers import data
from utils.excel_utils import read_excel
import logging
import allure

@allure.feature("用户模块")
@allure.story("登录功能")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("测试登录成功场景")

class TestRunner:
    #读测试数据
    data = read_excel()

    @pytest.mark.parametrize("case",data)
    def test_case(self,case):
        # print(case)
        logging.info(case)
        #数据解析：1、url不存在；2、部分字符串的值变为字典；3、预期结果不能在请求中传输，会报错
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
        # print(request_data)
        res = requests.request(**request_data)
        # print(res.json())
        assert res.json()['meta']['msg'] == case['expected']
