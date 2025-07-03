import time

import pytest
from data.test_data import *
from pages.buy_page import goodsPage
from config import LOGIN_URL, account, password
from pages.login_page import LoginPage


@pytest.mark.parametrize("title,should_pass",valid_cases)
def test_valid_cases(driver,title,should_pass):
    """
    商品添加购物车自动化
    :param driver: 浏览器驱动
    :param title: 测试商品标题
    :param should_pass: 是否测试成功
    """
    # 先登录
    login = LoginPage(driver)
    login.open(LOGIN_URL)
    login.input_account(account)
    login.input_password(password)
    login.click_login()
    login.main_page()
    # 进入商品详情页
    goods = goodsPage(driver)
    goods.open(title)
    goods.find_existing_spec_ids()
    #依次添加到购物车
    click_num = goods.add_all_color_size_to_cart()
    total = goods.to_goods_page()
    if should_pass:
        assert total == click_num
    else:
        assert total != click_num