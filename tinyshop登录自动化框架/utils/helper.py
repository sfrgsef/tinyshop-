from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 等待元素出现的工具函数
def wait_for_element(driver, by, value, timeout=10):
    """
    等待指定元素在页面上出现
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 超时时间（秒）
    :return: WebElement
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
def wait_visibility_of_element_located(driver, by, value, timeout=10):

    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))