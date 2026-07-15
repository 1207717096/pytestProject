# -*- coding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2026/7/12 19:22
@Author  : @叶风磊
@Desc    : 演示日志模块
"""
import logging

logging.basicConfig(level=logging.INFO)

logging.debug('这是一条调试信息')
logging.info('这是一条普通信息')
logging.warning('这是一条警告信息')
logging.error('这是一条错误信息')
logging.critical('这是一条严重信息')