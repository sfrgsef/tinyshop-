from selenium.webdriver.common.by import By

from utlis.helper import wait_p_element,wait_v_element


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

    def add_all_color_size_to_cart(self, found_spec_ids):
        """
        遍历所有组合，依次点击并加入购物车
        :param found_spec_ids: 包含所有类型的spec_id
        """
        all_lis = []
        for spec_ids in found_spec_ids:
            element_ul = self.driver.find_element(By.CSS_SELECTOR, f'ul.spec-values[spec_id="{spec_ids}"]')
            element_li = element_ul.find_elements(By.CSS_SELECTOR, 'li')
            all_lis.append(element_li)
            print(all_lis)
        success_count = self.click_all_lis(all_lis, 0, [])
        print(f"共成功添加 {success_count} 种组合")
        return success_count

    def click_all_lis(self, all_lis, click_lis, select_lis):
        """
           递归点击所有规格组合
           :param all_lis: 所有规格类型的选项列表
           :param click_lis: 当前处理的规格类型层级
           :param select_lis: 已选择的路径
        """
        if click_lis == len(all_lis):
            try:
                for element in select_lis:
                    if 'selected' in element.get_attribute('class'):
                        continue
                    if 'disabled' in element.get_attribute('class'):
                        continue
                    element.click()

                add_btn = self.driver.find_element(By.ID, 'add-cart')
                add_btn.click()
                return 1
            except Exception as e:
                print(e)
                return 0
        else:
            count = 0
            for option in all_lis[click_lis]:
                if 'disabled' in option.get_attribute('class'):
                    continue
                new_path = select_lis.copy()
                new_path.append(option)
                count += self.click_all_lis(all_lis,click_lis+1,new_path)
            return count

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






