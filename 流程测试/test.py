import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

username = "19710115706@qq.com"
password = "123123"
goumailiang = int(1) #购买量
shangpinming = "夏天职业衬衫女装正装短袖衬衫工装女寸衫韩版白领工作服白衬衣女"
dingdanbeizhu = "123123"
fapiaotaitou = "发票抬头"


def setup_driver():
    # 配置 Chrome 选项
    chrome_options = Options()
    # 选择无头模式
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--start-maximized')  # 最大化窗口
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式
    chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化标识
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 设置 ChromeDriver
    service = Service("D:\edgeqd\chromedriver-win64/chromedriver.exe")

    # 初始化 WebDriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def run():
    driver = setup_driver()
    try:

        url = "http://localhost:808/Tinyshop/"
        driver.get(url)
        print(f"成功打开网页: {url}")
#登录
        driver.find_element(By.XPATH, "//*[@class=\"normal\"][text()='登录']").click()
        driver.implicitly_wait(5)
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.ID, "account").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//*[@id=\"main\"]/div/div/form/ul/li[4]/button").click()

        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(), "会员中心") and @href="/Tinyshop/index.php?con=ucenter&act=index"]'))
        ).click()
        # 定位"账户管理"菜单下的"个人资料"
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//h2[text()="账户管理"]/following-sibling::ul//a[contains(text(), "个人资料")]'))
        ).click()

        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="info-form"]/table/tbody/tr[1]/td[2]'))
        )
        text_content = element.text
        print(text_content)

        time.sleep(10)
    except Exception as e:
        print(f"测试过程出现错误: {str(e)}")
    finally:
        # driver.quit()
        print(f"购买结束")

if __name__ == '__main__':
    run()
