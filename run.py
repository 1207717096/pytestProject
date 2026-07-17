import pytest
import os
from datetime import datetime
'''
4表示用于运行环境检测
__name__ 是一个内置变量，当文件被运行时，__name__就被设置为’__main__‘
当被导入到其他文件时，则判断条件不成立

'''

'''
os.system(命令)相当于在终端执行命令
allure generate 中间结果目录 -o 目标html报告目录 --clean
'''

if __name__ == '__main__':
    # 获取项目根目录（当前文件所在目录）
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    # 创建 report 目录（项目根目录下）
    report_dir = os.path.join(PROJECT_DIR, "report")
    allure_dir = os.path.join(PROJECT_DIR, "allure-results")
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(allure_dir, exist_ok=True)

    # 生成带时间戳的报告路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    allure_path = os.path.join(allure_dir, f"report_{timestamp}")
    html_allure_path = os.path.join(allure_path, "html_report")

    pytest.main(['-vs', './testcase/test_runner_40.py', f"--html={report_path}", "--alluredir", allure_path])

    # IDE 运行 Python 时通常不加载 ~/.zshrc，PATH 里可能没有 allure，所以用完整路径
    allure_bin = "/usr/local/allure-2.44.0/bin/allure"
    os.system(f"{allure_bin} generate {allure_path} -o {html_allure_path} --clean")