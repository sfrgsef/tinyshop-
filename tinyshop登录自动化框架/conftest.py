import pytest
from selenium import webdriver

@pytest.fixture(scope="function")  # 每个用例都新建driver
def driver():
    """
    提供每个用例独立的 selenium webdriver 实例，测试结束后自动关闭
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化标识
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--headless')  # 无界面模式
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # 设置隐式等待
    yield driver
    driver.quit()  # 关闭浏览器 