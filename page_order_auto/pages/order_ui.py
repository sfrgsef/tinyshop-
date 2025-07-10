import re
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from utils.hears import wait_p_element, is_element_exist
from utils.yaml_util import read_yaml


class order_ui(object):
    def __init__(self, driver):
        self.driver = driver
    #点击订单中心
    def order_click(self):
        element = wait_p_element(self.driver, By.LINK_TEXT, "订单中心")
        element.click()
    #点击上一页
    def order_previous(self):
        element = wait_p_element(self.driver, By.LINK_TEXT, '上一页')
        return element
    #点击下一页
    def order_next(self):
        element = wait_p_element(self.driver, By.LINK_TEXT, '下一页')
        return element
    #获取总页码
    def page_num(self):
        html = self.driver.page_source
        page_num = re.search("&nbsp;共(.*?) 页&nbsp;", html)
        return int(page_num.group(1))
    #点击确定
    def confirm_click(self):
        element = wait_p_element(self.driver, By.LINK_TEXT, "确定")
        element.click()


    #遍历页码
    def order_for(self):
        try:
            all_success = True
            now_page = wait_p_element(self.driver, By.XPATH, '//*[@id="content"]/div[1]/span[@class="current"]').text
            print(f"当前页码: {now_page}")
            page_num = self.page_num()
            print(f"总页码: {page_num}")
            for page_number in range(1, page_num+1):
                if int(now_page) == page_number:
                    print(f"已在{now_page}页码跳过:！")
                    continue
                else:
                    wait_p_element(self.driver, By.LINK_TEXT, f"{page_number}").click()
                    print(f"跳转到{page_number}页面: ")

                    current_url = self.driver.current_url
                    if str(page_number) in current_url:
                        print(f"成功跳转到{page_number}页")
                    else:
                        print(f"跳转{page_number}页失败")
                        all_success = False
            return all_success
        except Exception as e:
            print(f"遍历页码发现异常{e}")
            all_success = False
            return all_success

    #连续点击上一页
    def many_previous_click(self):
        try:
            all_success = True
            now_page = wait_p_element(self.driver, By.XPATH, '//*[@id="content"]/div[1]/span[@class="current"]').text
            print(f"当前页码: {now_page}")
            page_num = self.page_num()
            print(f"总页码: {page_num}")

            while True:
                element = self.order_previous()
                now_page = wait_p_element(self.driver, By.XPATH,
                                          '//*[@id="content"]/div[1]/span[@class="current"]').text

                element.click()
                current_url = self.driver.current_url
                now_page = int(now_page)-1
                if str(now_page) in current_url:
                    print(f"成功跳转到{now_page}页")
                    if now_page == 1:
                        print(f"已跳转到第{now_page}退出点击上一页")
                        break
                else:
                    print(f"跳转{now_page}页失败")
                    all_success = False
                    return all_success
        except Exception as e:
            print(f"连续点击上一页异常{e}")
            all_success = False
            return all_success
        return all_success



    # 连续点击下一页
    def many_next_click(self):
        try:
            all_success = True
            now_page = wait_p_element(self.driver, By.XPATH, '//*[@id="content"]/div[1]/span[@class="current"]').text
            print(f"当前页码: {now_page}")
            page_num = self.page_num()
            print(f"总页码: {page_num}")

            while True:
                now_page = wait_p_element(self.driver, By.XPATH,
                                          '//*[@id="content"]/div[1]/span[@class="current"]').text
                page_num = self.page_num()
                print(f"当前页码: {now_page}")
                if int(now_page) == int(page_num):
                    print(f"已到最后一页，退出点击下一页")
                    break
                else:
                    element = self.order_next()
                    now_page = int(now_page) + 1
                    print(f"即将要跳转到{now_page}页")
                    element.click()
                    current_url = self.driver.current_url

                    if str(now_page) in current_url:
                        print(f"成功跳转到{now_page}页")
                    else:
                        print(f"跳转{now_page}页失败")
                        all_success = False
                        return all_success
        except Exception as e:
            print(f"连续点击上一页异常{e}")
            all_success = False
            return all_success
        return all_success

    #输入框获取
    def input_page(self):
        element = wait_p_element(self.driver, By.XPATH, '//input[contains(@id, "page_input_")]')
        print(element.get_attribute('value'))
        return element


    #输入页数遍历
    def many_input_order(self):
        try:
            all_success = True
            pagenum = self.page_num()
            for page_number in range(1, pagenum+1):
                element = self.input_page()
                element.click()
                element.send_keys(Keys.CONTROL, 'a')
                element.send_keys(Keys.DELETE)
                element.send_keys(page_number)
                self.confirm_click()
                current_url = self.driver.current_url
                if str(page_number) in current_url:
                    print(f"成功跳转到{page_number}页")
                else:
                    print(f"跳转{page_number}页失败")
                    all_success = False
                    return all_success

        except Exception as e:
            print(f"输入页数遍历异常{e}")
            all_success = False
        return all_success


    #非法输入页数
    def valid_input_order(self):
        try:
            all_success = True
            novalid = read_yaml("./data/input_page.yaml")
            for value in novalid:
                element = self.input_page()
                element.clear()
                element.send_keys(value)
                self.confirm_click()
        except Exception as e:
            print(f"非法输入页数异常{e}")
            all_success = False
            return all_success
        return all_success
