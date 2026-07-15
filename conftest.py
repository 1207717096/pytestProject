#conftest.py

import os
import logging
import time
from datetime import datetime
import pytest

# ========== 日志配置 ==========

# 获取当前文件（conftest.py）所在目录，即项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 拼接 log 目录路径：项目根目录/log
LOG_DIR = os.path.join(BASE_DIR, "log")
# 创建 log 目录，exist_ok=True 表示目录已存在时不报错
os.makedirs(LOG_DIR, exist_ok=True)
# 生成当前时间戳，格式：年月日_时分秒，如 20260713_103815
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# 拼接完整日志文件路径：log/log_20260713_103815.log
LOG_FILE = os.path.join(LOG_DIR, f"log_{timestamp}.log")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    # 日志格式：文件名 代码行号 当前函数名 时间 [级别] 消息
    format="%(filename)-16s %(lineno)d %(funcName)s %(asctime)s [%(levelname)-3s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",    # 时间格式
    # 日志处理器列表
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"), # 文件处理器：输出到文件
        logging.StreamHandler() # 流处理器：输出到控制台
    ]
)
# 获取日志记录器实例
logger = logging.getLogger(__name__)


# ========== 收集运行数据 ==========
# 自定义类，用于存储整个测试运行的统计数据
class TestRunInfo:
    """存储测试运行整体信息"""

    def __init__(self):
        self.start_time = None      # 测试开始时间戳
        self.end_time = None        # 测试结束时间戳
        self.total_cases = 0        # 用例总数
        self.passed = 0             # 通过数
        self.failed = 0             # 失败数
        self.skipped = 0            # 跳过数
        self.errors = 0             # 错误数（setup/teardown 异常）
        self.case_details = []      # 每个用例的详细记录列表
        self.error_details = []     # 错误用例的详细信息列表

# 创建全局实例，所有钩子共享这个数据对象
run_info = TestRunInfo()


# ========== pytest 钩子 ==========

def pytest_sessionstart(session):
    """
        session: pytest 的 Session 对象，包含整个测试会话的信息
        """
    """测试会话开始"""
    # 记录开始时间戳（秒级）
    run_info.start_time = time.time()
    # 输出分隔线
    logger.info("=" * 60)
    # 标记测试开始
    logger.info("【测试执行开始】")
    # 记录开始时间（可读格式）
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # 尝试输出收集到的用例数（此时可能还未收集完）
    logger.info(f"收集到的测试用例数: {session.testscollected if hasattr(session, 'testscollected') else '待收集'}")
    logger.info("=" * 60)

# pytest 钩子：收集完所有测试用例后调用
def pytest_collection_modifyitems(session, config, items):
    """
    session: Session 对象
    config: pytest 配置对象
    items: 收集到的所有用例对象列表
    """
    """收集完用例后"""
    # 输出用例总数
    run_info.total_cases = len(items)
    # 遍历所有用例，输出用例名称
    logger.info(f"共收集到 {len(items)} 个测试用例")

    # 列出所有用例名称
    for item in items:
        # item.nodeid 是用例的唯一标识，格式：文件路径::类名::方法名
        logger.info(f"  - {item.nodeid}")

# @pytest.hookimpl(hookwrapper=True) 表示这是一个包装器钩子
# 包装器可以获取用例执行前后的上下文
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
        item: 当前执行的用例对象
        call: 调用阶段对象（setup/call/teardown）
        """
    # yield 将执行权交给 pytest，让 pytest 先执行用例
    # outcome 包含用例执行结果
    """每个用例执行后记录结果"""
    outcome = yield
    # 获取用例执行报告对象
    report = outcome.get_result()
    # 只处理 call 阶段（实际测试执行阶段，排除 setup 和 teardown）
    if report.when == "call":
        # 记录用例执行详情
        # 组装用例信息字典
        case_info = {
            "name": item.nodeid,  # 用例完整名称
            "status": report.outcome,  # 结果：passed/failed/skipped
            "duration": report.duration,  # 执行耗时（秒）
            "timestamp": datetime.now().strftime("%H:%M:%S")  # 执行时间
        }
        # 添加到用例详情列表
        run_info.case_details.append(case_info)

        # 统计结果
        # 根据结果分类统计
        if report.outcome == "passed":
            run_info.passed += 1  # 通过数 +1
        elif report.outcome == "failed":
            run_info.failed += 1  # 失败数 +1
            # 如果有错误信息，记录错误详情
            if report.longrepr:
                run_info.error_details.append({
                    "case": item.nodeid,
                    "error": str(report.longrepr)  # 错误堆栈信息
                })
        elif report.outcome == "skipped":
            run_info.skipped += 1  # 跳过数 +1

        # 输出每个用例的执行结果
        logger.info(f"【用例结果】{item.nodeid} | {report.outcome.upper()} | 耗时: {report.duration:.3f}s")

        # 如果用例失败，额外输出错误详情
        if report.outcome == "failed" and report.longrepr:
            logger.error(f"【错误详情】{item.nodeid}:\n{report.longrepr}")


# pytest 钩子：测试会话结束时调用
def pytest_sessionfinish(session, exitstatus):
    """
        session: Session 对象
        exitstatus: 退出状态码（0=全部通过，1=有失败，等）
        """
    """测试会话结束，输出整体统计"""
    # 记录结束时间戳
    run_info.end_time = time.time()
    # 计算总耗时
    total_time = run_info.end_time - run_info.start_time

    # 输出结束分隔线
    logger.info("=" * 60)

    # 标记测试结束
    logger.info("【测试执行结束】")

    # 输出结束时间
    logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 输出总耗时
    logger.info(f"总耗时: {total_time:.3f}s")

    # 输出统计分隔线
    logger.info("-" * 60)

    # 输出统计标题
    logger.info("【执行统计】")

    # 输出各项统计数据
    logger.info(f"  用例总数: {run_info.total_cases}")
    logger.info(f"  通过: {run_info.passed}")
    logger.info(f"  失败: {run_info.failed}")
    logger.info(f"  跳过: {run_info.skipped}")
    logger.info(f"  错误: {run_info.errors}")
    logger.info(
        f"  通过率: {run_info.passed / run_info.total_cases * 100:.1f}%" if run_info.total_cases > 0 else "  通过率: N/A")
    logger.info("-" * 60)

    # # 计算并输出通过率（避免除零）
    # if run_info.total_cases > 0:
    #     pass_rate = run_info.passed / run_info.total_cases * 100
    #     logger.info(f"  通过率: {pass_rate:.1f}%")
    # else:
    #     logger.info("  通过率: N/A")
    #
    # logger.info("-" * 60)

    # 失败用例汇总
    # 计算并输出通过率（避免除零）
    if run_info.failed > 0:
        logger.info("【失败用例汇总】")
        for detail in run_info.error_details:
            logger.error(f"  ✗ {detail['case']}")

    logger.info("=" * 60)