import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_ui import login_ui
from pages.order_ui import order_ui
@pytest.fixture(scope='session')
def driver():

    options = Options()
    # options.add_argument('--headless')  # 无界面模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化标识
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 创建WebDriver实例
    driver = webdriver.Chrome(options=options)
    try:
        login_ui(driver).open()
        while True:
            # 输入验证码
            print("请输入验证码：")
            v_code_url = input()
            login_ui(driver).login(v_code_url)
            current = driver.current_url
            if "act=index" in current:
                print("登录成功！！")
                break
            else:
                print("验证码错误请再次输入")
    except Exception as e:
        print(f"登录失败{e}")
    time.sleep(2)
    order_pages = order_ui(driver)
    order_pages.order_click()

    yield driver

    driver.quit()
