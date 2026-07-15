import jsonpath
import pytest
import requests

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

    @pytest.mark.parametrize("login_data",login_data)
    def test_login(self,login_data):
        print("test_report")
        res = requests.request(**login_data)
        print(res.json())

    @pytest.mark.parametrize("user_list_data",user_list_data)
    def test_user_list(self,user_list_data):
        print("test_user_list")
        #调用获取token的函数拿到token值
        token = get_token()
        #组装header，让请求头中具有token
        user_list_data['headers'] = {'Authorization': token}
        res = requests.request(**user_list_data)
        print(res.json())