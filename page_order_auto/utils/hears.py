from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_p_element(driver, by,value,timeout=10):
    """
    param by:定位方式
    param value:元素信息
    param timeout:等待超时时间
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_v_element(driver, by,value,timeout=10):
    """
    param by:定位方式
    param value:元素信息
    param timeout:等待超时时间
    """
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))
def is_element_exist(driver,xpath,timeout = 10):
    """
    param xpath:判断该元素是否存在
    """
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except:
        return False