import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from config import LOGIN_URL
from pages.login_page import LoginPage

# 有效和无效等价类测试用例
valid_cases = [
    ("text@qq.com", "abc123", True),  # 有效账号密码
    ("", "abc123", False),
    ("text1@qq.com", "abc123", False),
    ("Text@qq.com", "abc123", False),
    ("   text@qq.com", "abc123", True),
    ("te xt@qq.com", "abc123", False),
    ("text@qq.com  ", "abc123", False),
    ("text@qq.com", "abc123123", False),
    ("text@qq.com", "Abc123", False),
    ("text@qq.com", "  abc123", False),
    ("text@qq.com", "abc  123", False),
    ("text@qq.com", "abc123  ", False)
]
@pytest.mark.parametrize("account,password,should_pass", valid_cases)
def test_login(driver, account, password, should_pass):
    """
    登录功能自动化测试
    :param driver: 浏览器驱动
    :param account: 测试账号
    :param password: 测试密码
    :param should_pass: 是否应登录成功
    """
    login = LoginPage(driver)
    login.open(LOGIN_URL)
    login.input_account(account)
    login.input_password(password)
    login.click_login()
    if should_pass:
        # 登录成功：断言页面已跳转到非登录页（如URL不再包含login）
        assert "login" not in driver.current_url.lower()
    else:
        # 登录失败：断言页面仍为登录页或有错误提示
        try:
            # 账号输入框还在，说明还在登录页
            assert driver.find_element(By.ID, "account").is_displayed()
        except NoSuchElementException:
            # 或页面URL仍包含login
            assert "login" in driver.current_url.lower() 