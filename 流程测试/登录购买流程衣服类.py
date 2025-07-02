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
#搜索商品
        driver.find_element(By.ID, "search-keyword").send_keys(shangpinming)
        driver.find_element(By.CLASS_NAME, "btn-search ").click()
#选择商品类型

        driver.find_element(By.XPATH,"//*[@id=\"main\"]/div[2]/div/div/div[2]/dl/dd/ul/li/dl/dt/a/img").click()

        yanse = driver.find_element(By.XPATH, "//*[@id=\"product-intro\"]/div[3]/div/dl[1]/dd/ul/li[1]")
        yanseclass = yanse.get_attribute("class")
        if "disabled" in yanseclass:
            result = "商品库存不足"
            print(result)
            return result

        driver.find_element(By.XPATH,"//*[@id=\"product-intro\"]/div[3]/div/dl[1]/dd/ul/li[1]/span").click()

        cima = driver.find_element(By.XPATH, "//*[@id=\"product-intro\"]/div[3]/div/dl[2]/dd/ul/li[1]")
        cimaclass = cima.get_attribute("class")
        if "disabled" in cimaclass:
            result = "商品库存不足"
            print(result)
            return result

        driver.find_element(By.XPATH, "//*[@id=\"product-intro\"]/div[3]/div/dl[2]/dd/ul/li[1]/span").click()

#选择商品数量

        inputsl = driver.find_element(By.ID, "buy-num")
        inputsl.send_keys(Keys.CONTROL, "a")
        inputsl.send_keys(Keys.DELETE)


        inputsl.send_keys(goumailiang)
#添加等待，等元素加载之后获取
        element = wait.until(EC.visibility_of_element_located((By.ID, "store_nums")))
        store_nums = int(element.text)
        print("商品库存为：",store_nums)
        if goumailiang>store_nums:
            result = "商品购买量大于库存量,已改为最大库存量"
            print(result)

        driver.find_element(By.ID, "buy-now").click()

#立即结算
        driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[2]/div[2]/p/a[2]").click()
        driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[2]/div/form/div[1]/ul/li[1]").click()
#提交订单
        driver.find_element(By.NAME, "user_remark").send_keys(dingdanbeizhu)
        driver.find_element(By.ID, "is_invoice").click()
        driver.find_element(By.NAME, "invoice_title").send_keys(fapiaotaitou)
        driver.find_element(By.CSS_SELECTOR, "input.btn.btn-main.fr").click()


# 支付
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.btn-main"))).click()
        # 记录点击前的窗口句柄
        original_window = driver.current_window_handle
        if WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 0):
            # 获取所有窗口句柄
            windows = driver.window_handles

            # 切换到新窗口（不是原始窗口的那个）
            for window in windows:
                if window != original_window:
                    driver.switch_to.window(window)
                    print("已切换到新窗口")
                    break

        # 检查支付结果
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.btn-main")))
            print("购买成功")
        except TimeoutException:
            print("余额不足")
        except Exception as e:
            print(f"购买错误: {str(e)}")


    except Exception as e:
        print(f"测试过程出现错误: {str(e)}")
    finally:
        #driver.quit()
        print(f"购买结束")


if __name__ == '__main__':
    run()
