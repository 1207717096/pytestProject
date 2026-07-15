import pytest
from utils.allure_utils import allure_report_init
from jinja2 import Template
from pygments.lexers import data
from utils.analyse_case import analyse_case
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor
from utils.asserts import *


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
        request_data = analyse_case(case)

        # 核心步骤2：发起请求，得到响应结果
        res = send_http_request(**request_data)
        # res = requests.request(**request_data)

        # 核心步骤3：处理断言
        #HTTP响应断言
        http_assert(case,res)
        #数据库断言
        jdbc_assert(case)
        #json提取
        json_extractor(case,all,res)
        #数据库提取
        jdbc_extractor(case,all)