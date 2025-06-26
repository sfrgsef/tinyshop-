import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def browser():
    """创建浏览器实例的fixture"""
    # 配置Chrome选项
    options = Options()
    options.add_argument('--start-maximized')  # 最大化窗口
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument('--no-sandbox')  # 禁用沙盒模式
    options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化标识
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # 使用webdriver-manager自动管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # 设置隐式等待时间
        driver.implicitly_wait(10)
        
        # 执行JavaScript来隐藏webdriver属性
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        yield driver
        
    except Exception as e:
        print(f"浏览器启动失败: {e}")
        raise
    finally:
        # 确保浏览器被正确关闭
        try:
            driver.quit()
        except:
            pass 