# -*- coding: utf-8 -*-
"""
@File    : allure_utils.py
@Time    : 2026/7/14 17:09
@Author  : @叶风磊
@Desc    : allure测试报告的工具封装
"""
import allure


def allure_report_init(case):

    allure.dynamic.feature(case["feature"])
    allure.dynamic.story(case["story"])
    allure.dynamic.title(f'用例ID:{case["id"]}--{case["title"]}')


