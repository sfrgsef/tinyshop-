from selenium.webdriver.common.by import By
from data.configpy import *


class login_ui:
    def __init__(self, driver):
        self.driver = driver
    def open(self):
        self.driver.get(V_CODE_URL)
    def html(self):
        return self.driver.page_source

    def login(self,v_code_url):
        driver = self.driver
        element = driver.find_element(By.NAME, "name")
        element.clear()
        element.send_keys(NAME)
        element = driver.find_element(By.NAME, "password")
        element.clear()
        element.send_keys(PASSWORD)

        element = driver.find_element(By.NAME, "verifyCode")
        element.clear()
        element.send_keys(v_code_url)

        element = driver.find_element(By.CSS_SELECTOR, "button" and "input[value='登 录']")
        element.click()