#!/bin/bash


# 设置错误时退出
set -e

echo "========== 开始安装 Python 依赖 =========="

#下面两个命令是更换国内的pip源，推荐执行；执行的时候可以取消注释
#pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple

 #pip3 config set install.trusted-host mirrors.aliyun.com

# 升级 pip 本身
pip3 install --upgrade pip

# 安装核心依赖
pip3 install requests
pip3 install pytest
pip3 install pytest-html
pip3 install pytest-ordering
pip3 install allure-pytest

# 安装数据库相关
pip3 install pymysql
pip3 install openpyxl

# 安装工具库
pip3 install jinja2
pip3 install jsonpath
pip3 install pytest-rerunfailures

echo "========== 安装完成 =========="

# 验证安装
echo "已安装包列表："
pip list