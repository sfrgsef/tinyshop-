import time
import logging
import pytest
import allure
from data.test_data import *
from pages.buy_page import goodsPage
from config import LOGIN_URL, account, password
from pages.login_page import LoginPage

# 配置日志
logger = logging.getLogger(__name__)

@allure.epic("商品购物车自动化测试")
@allure.feature("商品添加购物车功能")
@pytest.mark.parametrize("title,should_pass", valid_cases)
def test_valid_cases(driver, title, should_pass):
    """
    商品添加购物车自动化
    :param driver: 浏览器驱动
    :param title: 测试商品标题
    :param should_pass: 是否测试成功
    """
    with allure.step(f"开始测试商品: {title}"):
        logger.info(f"开始测试商品: {title}")
        
        # 先登录
        with allure.step("用户登录"):
            logger.info("开始用户登录流程")
            login = LoginPage(driver)
            login.open(LOGIN_URL)
            login.input_account(account)
            login.input_password(password)
            login.click_login()
            login.main_page()
            logger.info("用户登录完成")
        
        # 进入商品详情页
        with allure.step("进入商品详情页"):
            logger.info(f"进入商品详情页: {title}")
            goods = goodsPage(driver)
            goods.open(title)
            goods.find_existing_spec_ids()
        
        # 依次添加到购物车
        with allure.step("添加商品到购物车"):
            logger.info("开始添加商品到购物车")
            click_num = goods.add_all_color_size_to_cart()
            logger.info(f"点击加入购物车次数: {click_num}")
        
        with allure.step("验证购物车商品数量"):
            logger.info("验证购物车商品数量")
            total = goods.to_goods_page()
            logger.info(f"购物车实际商品数量: {total}")
            
            if should_pass:
                assert total == click_num, f"期望数量: {click_num}, 实际数量: {total}"
                logger.info("测试通过: 购物车商品数量正确")
            else:
                assert total != click_num, f"期望数量不等于: {click_num}, 实际数量: {total}"
                logger.info("测试通过: 购物车商品数量验证正确")