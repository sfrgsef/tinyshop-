import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# 配置日志
logger = logging.getLogger(__name__)

def wait_p_element(driver, by, value, timeout=10):
    """
    等待元素在页面上出现（presence）
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 等待时间
    :return: WebElement
    """
    try:
        logger.debug(f"等待元素出现: {by}={value}, 超时时间: {timeout}秒")
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        logger.debug(f"元素已出现: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"等待元素超时: {by}={value}, 超时时间: {timeout}秒")
        raise
    except WebDriverException as e:
        logger.error(f"等待元素时发生WebDriver错误: {by}={value}, 错误: {e}")
        raise

def wait_v_element(driver, by, value, timeout=10):
    """
    等待元素在页面上可见（visibility）
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 等待时间
    :return: WebElement
    """
    try:
        logger.debug(f"等待元素可见: {by}={value}, 超时时间: {timeout}秒")
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        logger.debug(f"元素已可见: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"等待元素可见超时: {by}={value}, 超时时间: {timeout}秒")
        raise
    except WebDriverException as e:
        logger.error(f"等待元素可见时发生WebDriver错误: {by}={value}, 错误: {e}")
        raise

def wait_c_element(driver, by, value, timeout=10):
    """
    等待元素可点击（clickable）
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 等待时间
    :return: WebElement
    """
    try:
        logger.debug(f"等待元素可点击: {by}={value}, 超时时间: {timeout}秒")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        logger.debug(f"元素可点击: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"等待元素可点击超时: {by}={value}, 超时时间: {timeout}秒")
        raise
    except WebDriverException as e:
        logger.error(f"等待元素可点击时发生WebDriver错误: {by}={value}, 错误: {e}")
        raise

def safe_click(driver, by, value, timeout=10):
    """
    安全点击元素（等待元素可点击后点击）
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param timeout: 等待时间
    """
    try:
        element = wait_c_element(driver, by, value, timeout)
        logger.info(f"点击元素: {by}={value}")
        element.click()
    except Exception as e:
        logger.error(f"点击元素失败: {by}={value}, 错误: {e}")
        raise

def safe_input(driver, by, value, text, timeout=10):
    """
    安全输入文本（等待元素出现后输入）
    :param driver: selenium webdriver 实例
    :param by: 定位方式
    :param value: 定位值
    :param text: 要输入的文本
    :param timeout: 等待时间
    """
    try:
        element = wait_p_element(driver, by, value, timeout)
        element.clear()
        logger.info(f"输入文本到元素: {by}={value}, 文本: {text}")
        element.send_keys(text)
    except Exception as e:
        logger.error(f"输入文本失败: {by}={value}, 文本: {text}, 错误: {e}")
        raise