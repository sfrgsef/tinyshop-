from selenium import webdriver
from selenium.webdriver.common.by import By

from utlis.helper import wait_p_element,wait_v_element
from data.test_data import *


class goodsPage:
    """
    进入商品详情页
    """
    def __init__(self,driver):
        self.driver = driver

    def open(self, title):
        """
        打开指定标题的商品详情页
        :param title: 商品标题
        """
        elem = wait_p_element(self.driver, By.LINK_TEXT, title)
        elem.click()

    def find_existing_spec_ids(self, min_id=1, max_id=8):
        """
        优化：一次性查找所有ul.spec-values，减少Selenium查找次数
        """
        found_spec_ids = []
        ul_elements = self.driver.find_elements(By.CSS_SELECTOR, 'ul.spec-values')
        for ul in ul_elements:
            spec_id = ul.get_attribute('spec_id')
            if spec_id and spec_id.isdigit():
                spec_id_int = int(spec_id)
                if min_id <= spec_id_int <= max_id:
                    found_spec_ids.append(spec_id_int)
                    print(f"找到spec_id={spec_id_int}的商品规格")
        return found_spec_ids

    def add_all_color_size_to_cart(self, color_spec_id=2, size_spec_id=6):
        """
        遍历所有颜色和尺码组合，依次点击并加入购物车
        :param color_spec_id: 颜色的spec_id
        :param size_spec_id: 尺码的spec_id
        """
        color_ul = self.driver.find_element(By.CSS_SELECTOR, f'ul.spec-values[spec_id="{color_spec_id}"]')
        size_ul = self.driver.find_element(By.CSS_SELECTOR, f'ul.spec-values[spec_id="{size_spec_id}"]')
        color_lis = color_ul.find_elements(By.TAG_NAME, 'li')
        size_lis = size_ul.find_elements(By.TAG_NAME, 'li')
        click_num = 0
        for color_li in color_lis:
            color_text = color_li.text
            color_li.click()
            for size_li in size_lis:
                size_text = size_li.text
                size_li.click()
                print(f"选择颜色: {color_text}, 尺码: {size_text}，点击加入购物车")
                add_btn = self.driver.find_element(By.ID, 'add-cart')
                add_btn.click()
                click_num += 1
        print(f"<UNK>{click_num}<UNK>")
        return click_num

    def to_goods_page(self):
        # 先向上滚动页面
        self.driver.execute_script("window.scrollTo(0, 0);")
        # 再向下滚动页面
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 点击购物车图标
        self.driver.find_element(By.CLASS_NAME, 'icon-cart-32').click()
        wait_p_element(self.driver,By.LINK_TEXT, '去购物车结算').click()
        # 先向上滚动页面
        self.driver.execute_script("window.scrollTo(0, 0);")
        # 再向下滚动页面
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 获取所有name='buy_num'的input元素，累加其value
        input_elements = self.driver.find_elements(By.NAME, 'buy_num')
        total = 0
        for elem in input_elements:
            value = elem.get_attribute('value')
            if value and value.isdigit():
                total += int(value)
        print(f"buy_num总和: {total}")
        return total






