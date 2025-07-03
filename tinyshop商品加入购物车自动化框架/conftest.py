import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 无界面模式
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # 设置隐式等待
    yield driver
    driver.quit()  # 关闭浏览器