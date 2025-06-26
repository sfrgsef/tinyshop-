"""
测试配置文件
用于管理测试参数和设置
"""

# 导入必要的模块
from selenium.webdriver.common.by import By

# 测试网站配置
TEST_URLS = {
    "baidu_home": "https://www.baidu.com",
}

# 浏览器配置
BROWSER_CONFIG = {
    "implicit_wait": 10,  # 隐式等待时间（秒）
    "page_load_timeout": 30,  # 页面加载超时时间（秒）
    "script_timeout": 30,  # 脚本执行超时时间（秒）
}

# 测试数据
TEST_DATA = {
    "search_keywords": [
        "Python自动化测试",
        "Selenium自动化",
        "Pytest测试框架",
        "百度搜索测试",
    ],
    "special_characters": "Python@#$%^&*()",
    "empty_search": "",
}

# 元素定位器
LOCATORS = {
    "search_box": (By.ID, "kw"),
    "search_button": (By.ID, "su"),
    "search_results": (By.ID, "content_left"),
    "search_suggestions": (By.CLASS_NAME, "bdsug"),
}

# 测试报告配置
REPORT_CONFIG = {
    "report_dir": "test_reports",
    "report_prefix": "baidu_test_report",
    "auto_open_browser": True,
}

# 测试超时配置
TIMEOUT_CONFIG = {
    "element_wait": 10,  # 元素等待时间（秒）
    "page_load": 30,  # 页面加载等待时间（秒）
}

# 调试配置
DEBUG_CONFIG = {
    "headless": False,  # 是否使用无头模式
    "screenshot_on_failure": True,  # 失败时是否截图
    "verbose_output": True,  # 是否输出详细信息
} 