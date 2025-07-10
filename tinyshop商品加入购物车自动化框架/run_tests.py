#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
用于执行测试并生成 Allure HTML 报告
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import shutil

ALLURE_PATH = r"D:\allure\allure-2.34.1\bin\allure.bat"

def run_tests():
    """运行测试并生成报告"""
    
    # 创建报告目录
    reports_dir = "./reports"
    allure_results_dir = f"{reports_dir}/allure-results"
    allure_report_dir = f"{reports_dir}/allure-report"
    log_file = f"{reports_dir}/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(allure_results_dir, exist_ok=True)
    
    print("=" * 60)
    print("开始执行自动化测试...")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 运行 pytest 测试
        print("正在运行测试...")
        cmd = [
            sys.executable, "-m", "pytest",
            "--alluredir", allure_results_dir,
            "-vs",
            "--tb=short",
            "--capture=tee-sys",
            f"--log-file={log_file}",
            "--log-file-level=INFO"
        ]
        # 清空目录（确保目录存在且为空）
        if os.path.exists(allure_results_dir):
            shutil.rmtree(allure_results_dir)
        os.makedirs(allure_results_dir, exist_ok=True)

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        # 打印测试输出
        if result.stdout:
            print("测试输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        print(f"测试执行完成，退出码: {result.returncode}")
        print(f"日志文件已保存: {log_file}")
        
        # 生成 HTML 报告（使用绝对路径调用 allure）
        if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
            print("\n正在生成 HTML 报告...")
            report_cmd = [
                ALLURE_PATH, "generate",
                allure_results_dir,
                "-o", allure_report_dir,
                "--clean"
            ]
            subprocess.run(report_cmd, check=True)
            
            # 打开报告
            open_cmd = [ALLURE_PATH, "open", allure_report_dir]
            print(f"\nHTML 报告已生成: {allure_report_dir}")
            print("正在打开报告...")
            subprocess.Popen(open_cmd)
            
        else:
            print("警告: 没有找到测试结果数据")
            print(f"检查目录: {allure_results_dir}")
        
        print("=" * 60)
        print(f"测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return result.returncode
        
    except Exception as e:
        print(f"执行测试时发生错误: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 