import pytest
import logging
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s [%(name)s:%(lineno)s] : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    """浏览器驱动 fixture"""
    logger.info("初始化浏览器驱动")
    
    options = Options()
    # options.add_argument('--headless')  # 无界面模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化标识
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 添加日志记录
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)  # 设置隐式等待
        logger.info("浏览器驱动初始化成功")
        
        # 添加 allure 附件
        allure.attach(
            name="浏览器信息",
            body=f"Chrome 版本: {driver.capabilities.get('browserVersion', 'Unknown')}\n"
                 f"ChromeDriver 版本: {driver.capabilities.get('chrome', {}).get('chromedriverVersion', 'Unknown')}",
            attachment_type=allure.attachment_type.TEXT
        )
        
        yield driver
        
    except Exception as e:
        logger.error(f"浏览器驱动初始化失败: {e}")
        raise
    finally:
        logger.info("关闭浏览器驱动")
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"关闭浏览器时发生错误: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """为测试用例添加截图附件"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get("driver")
            if driver:
                # 截图
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # 页面源码
                page_source = driver.page_source
                allure.attach(
                    page_source,
                    name="页面源码",
                    attachment_type=allure.attachment_type.HTML
                )
                
                logger.info("已添加失败截图和页面源码到报告")
        except Exception as e:
            logger.warning(f"添加附件时发生错误: {e}")