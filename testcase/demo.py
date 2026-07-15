# -*- coding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2026/7/14 14:55
@Author  : @叶风磊
@Desc    : 
"""
from wsgiref import headers

import requests
import jsonpath

#实现：初始化数据
login_data = {
    "method":"post",
    "url":"http://127.0.0.1:8888/api/private/v1/login",
    "params": None,
    "data":{
        "username":"admin",
        "password":"admin"
    },
    "json":None,
    "files":None,
    "headers": None,
}

upload_data = {
    "method":"post",
    "url":"http://127.0.0.1:8888/api/private/v1/upload",
    "params": None,
    "files":None,
    "headers": None
}

res1 = requests.request(**login_data)
print(res1.json())

#2、提取token
#方法1：
# token1 = res1.json()['data']['token']

#方法2：jsonpath库进行提取想要的字段值；jsonpath.jsonpath（字典数据，jsonpath表达式），返回的是一个列表
token2 = jsonpath.jsonpath(res1.json(),'$..token')[0]

#3、获取用户数据列表
upload_data['headers'] = {"Authorization": token2}
#files 对应的值类似于{参数名：元组}
    #参数名在接口文档中会给
    #参数值元组（参数1，参数2，参数3）
        #第一个参数，上传服务器时用的文件名
        #第二个参数，用open()函数打开的文件对象
        #第三个参数，文件类型

upload_data['files'] = {'file':('picture.png',open('./files/picture.png','rb'),'png')}
res2 = requests.request(**upload_data)
print(res2.json())