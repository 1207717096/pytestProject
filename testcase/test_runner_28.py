import jsonpath
import pytest
import requests
from pygments.lexers import data

data = [
    {
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
    },{
        "method":"get",
        "url":"http://127.0.0.1:8888/api/private/v1/users",
        "params": {
            "query":"admin",
            "pagenum":1,
            "pagesize":10,
        },
        "data":None,
        "json":None,
        "files":None,
        "headers": None,
    }
]

login_data = [{
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
}]

user_list_data = [{
    "method":"get",
    "url":"http://127.0.0.1:8888/api/private/v1/users",
    "params": {
        "query":"admin",
        "pagenum":1,
        "pagesize":10,
    },
    "data":None,
    "json":None,
    "files":None,
    "headers": None,
}]

def get_token():
    res = requests.request(**login_data[0])
    token = jsonpath.jsonpath(res.json(), '$..token')
    return token

class TestRunner:
    @pytest.mark.parametrize("data",data)
    def test_case(self,data):
        res = requests.request(**data)
        print(res.json())
