#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2C Tiny Shop API自动化测试 - Windows Allure版本
专门为Windows环境优化，使用allure.bat命令
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.logger import logger
from config.conf import load_config


def run_windows_tests():
    # 加载配置
    config = load_config()
    logger.info("成功加载YAML文件: config/conf.yaml")
    
    # 清理历史报告
    allure_raw_dir = Path("reports/allure_raw")
    if allure_raw_dir.exists():
        shutil.rmtree(allure_raw_dir)
    logger.info("已清理历史报告")

    # 直接用Python调用你的测试主流程
    from tests.test_api_auto import TestAPIAuto
    test_runner = TestAPIAuto()
    test_runner.setup_class()
    for test_file in test_runner.test_data_files:
        test_runner.test_api_cases(test_file)
    test_runner.teardown_class()

    # 生成Allure报告
    logger.info("开始生成Allure报告...")
    from utils.allure_utils import generate_allure_report
    generate_allure_report("reports/allure_raw", "reports/allure")
    logger.info("Allure报告生成成功")

    # 输出测试统计
    logger.info("=" * 50)
    logger.info("测试执行完成")
    os.system("allure.bat open reports/allure")

if __name__ == "__main__":
    logger.info("测试会话开始")
    
    try:
        total, passed, failed = run_windows_tests()
        
        # 设置退出码
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"测试执行过程中发生错误: {e}")
        exit_code = 1
        
    finally:
        logger.info("测试会话结束，退出状态: " + str(exit_code))
        
    sys.exit(exit_code) 