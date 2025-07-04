#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境配置验证脚本
检查 pytest/selenium 环境是否正确配置
"""

import sys
import subprocess
import importlib

def check_python_packages():
    """检查 Python 包是否已安装"""
    print("=" * 50)
    print("检查 Python 包...")
    print("=" * 50)
    
    required_packages = [
        'pytest',
        'allure-pytest',
        'selenium'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("\n✅ 所有必需的 Python 包都已安装")
    return True

def check_chrome_driver():
    """检查 ChromeDriver 是否可用"""
    print("\n" + "=" * 50)
    print("检查 ChromeDriver...")
    print("=" * 50)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        version = driver.capabilities.get('browserVersion', 'Unknown')
        driver.quit()
        
        print(f"✅ ChromeDriver 可用")
        print(f"   Chrome 版本: {version}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver 不可用: {e}")
        print("\n请确保:")
        print("1. Chrome 浏览器已安装")
        print("2. ChromeDriver 已安装并与 Chrome 版本匹配")
        print("3. ChromeDriver 在系统 PATH 中")
        return False

def run_test_config():
    """运行配置测试"""
    print("\n" + "=" * 50)
    print("运行配置测试...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'testcases', 
            '--alluredir', './reports/allure-results',
            '-v'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 配置测试通过")
            print("\n测试输出:")
            print(result.stdout)
            return True
        else:
            print("❌ 配置测试失败")
            print("\n错误输出:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 配置测试超时")
        return False
    except Exception as e:
        print(f"❌ 运行配置测试时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("🔍 开始验证 pytest/selenium 环境配置...")
    
    checks = [
        check_python_packages,
        check_chrome_driver,
        run_test_config
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查都通过了！环境配置正确。")
        print("\n现在你可以运行测试:")
        print("  python run_tests.py")
        print("  或")
        print("  run_tests.bat (Windows)")
    else:
        print("⚠️  部分检查失败，请根据上述提示修复问题。")
    print("=" * 50)

if __name__ == "__main__":
    main() 