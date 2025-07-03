from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_p_element(driver, by, value, timeout=10):
    """""
    等待自动化元素在羊肉面上出现
    :param driver:selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 等待时间
    :return:WebElement
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
def wait_v_element(driver, by, value, timeout=10):
    """""
        等待自动化元素在羊肉面上出现
        :param driver:selenium webdriver 实例
        :param by: 定位方式
        :param value: 定位值
        :param timeout: 等待时间
        :return:WebElement
        """
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))