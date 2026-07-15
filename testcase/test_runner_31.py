'''
使用伪代码来表示执行自动化测试的业务过程

'''
from unittest import case

import jsonpath
import pytest
import requests
from pygments.lexers import data
from utils.excel_utils import read_excel
import logging
class TestRunner:
    #读取测试用例文件中的全部数据，用属性保存即可
    data = read_excel()

    #提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典

    #参数化的内容
    @pytest.mark.parametrize("case",data)
    def test_case(self,case):
        pass
        #核心步骤1：解析请求参数
        #核心步骤2：发起请求，得到响应结果
        #核心步骤3：处理断言
        #核心步骤4，提取所需的数据
