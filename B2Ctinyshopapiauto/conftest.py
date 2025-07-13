import pytest
import os
import allure
from core.logger import logger
from core.variable_pool import variable_pool
from config.conf import config

@pytest.fixture(scope="session")
def api_config():
    """API配置fixture"""
    return config

@pytest.fixture(scope="session")
def variable_pool_fixture():
    """变量池fixture"""
    return variable_pool

@pytest.fixture(autouse=True)
def setup_test_environment():
    """设置测试环境"""
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/allure_raw", exist_ok=True)
    
    logger.info("测试环境设置完成")
    yield
    logger.info("测试环境清理完成")

@pytest.fixture(scope="function")
def allure_environment():
    """Allure环境信息"""
    return {
        "Base_URL": config.get("base_url", ""),
        "Environment": "Test",
        "Framework": "pytest",
        "Python_Version": "3.x"
    }

@pytest.fixture(scope="function")
def clean_variables():
    """清理变量池"""
    yield
    variable_pool.clear()
    logger.info("变量池已清理")

def pytest_configure(config):
    """pytest配置"""
    # 添加自定义标记
    config.addinivalue_line("markers", "api_test: API自动化测试")
    config.addinivalue_line("markers", "auth: 认证相关测试")
    config.addinivalue_line("markers", "goods: 商品相关测试")
    config.addinivalue_line("markers", "order: 订单相关测试")
    config.addinivalue_line("markers", "system: 系统相关测试")

def pytest_collection_modifyitems(config, items):
    """修改测试用例收集"""
    for item in items:
        # 根据文件路径添加标记
        file_path = str(item.fspath)
        if "auth" in file_path:
            item.add_marker(pytest.mark.auth)
        elif "goods" in file_path:
            item.add_marker(pytest.mark.goods)
        elif "order" in file_path:
            item.add_marker(pytest.mark.order)
        elif "system" in file_path:
            item.add_marker(pytest.mark.system)

def pytest_runtest_setup(item):
    """测试用例执行前设置"""
    logger.info(f"开始执行测试: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """测试用例执行后清理"""
    logger.info(f"完成执行测试: {item.name}")

def pytest_sessionstart(session):
    """测试会话开始"""
    logger.info("测试会话开始")

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束"""
    logger.info(f"测试会话结束，退出状态: {exitstatus}")