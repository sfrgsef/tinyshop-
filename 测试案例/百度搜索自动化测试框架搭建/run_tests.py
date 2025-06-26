#!/usr/bin/env python3
"""
百度搜索自动化测试运行脚本
用于执行测试并生成HTML测试报告
"""

import os
import sys
import subprocess
from datetime import datetime

def run_tests():
    """运行测试并生成报告"""
    
    # 创建报告目录
    report_dir = "test_reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # 生成报告文件名（包含时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"baidu_test_report_{timestamp}.html")
    
    # 构建pytest命令
    cmd = [
        sys.executable, "-m", "pytest",
        "test_baidu_search.py",  # 测试文件
        "-v",  # 详细输出
        "--html=" + report_file,  # HTML报告
        "--self-contained-html",  # 自包含的HTML
        "--capture=no",  # 显示print输出
        "--tb=short",  # 简短的错误回溯
    ]
    
    print("开始运行百度搜索自动化测试...")
    print(f"测试报告将保存到: {report_file}")
    print("-" * 50)
    
    try:
        # 运行测试
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("-" * 50)
        if result.returncode == 0:
            print("✅ 所有测试通过！")
        else:
            print("❌ 部分测试失败，请查看详细报告")
        
        print(f"📊 测试报告已生成: {report_file}")
        
        # 尝试在浏览器中打开报告
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(report_file)}")
            print("🌐 已在浏览器中打开测试报告")
        except:
            print("无法自动打开报告，请手动打开HTML文件")
            
    except Exception as e:
        print(f"❌ 运行测试时发生错误: {e}")
        return False
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 