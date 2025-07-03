from selenium.webdriver.common.by import By
from utlis.helper import wait_p_element,wait_v_element

class LoginPage:
    """
    登录页面对象，封装登录相关操作
    """
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        """打开登录页面"""
        self.driver.get(url)

    def input_account(self, account):
        """输入账号"""
        wait_v_element(self.driver, By.ID, "account").clear()
        self.driver.find_element(By.ID, "account").send_keys(account)

    def input_password(self, password):
        """输入密码"""
        wait_v_element(self.driver, By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)

    def click_login(self):
        """点击登录按钮"""
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-main").click()

    def main_page(self):
        """点击首页"""
        self.driver.find_element(By.LINK_TEXT, "首页").click()
