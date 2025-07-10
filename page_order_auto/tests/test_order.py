import pytest
from pages.order_ui import order_ui  # 导入页面类

# 遍历页码
def test_order_for(driver):
    order_page = order_ui(driver)
    result = order_page.order_for()
    assert result

# 连续点击上一页
def test_many_previous_click(driver):
    order_page = order_ui(driver)
    result = order_page.many_previous_click()
    assert result

# 连续点击下一页
def test_many_next_click(driver):
    order_page = order_ui(driver)
    result = order_page.many_next_click()
    assert result

# 输入框获取
def test_input_page(driver):
    order_page = order_ui(driver)
    result = order_page.input_page()
    assert result

# 输入页数遍历
def test_many_input_order(driver):
    order_page = order_ui(driver)
    result = order_page.many_input_order()
    assert result
# 非法输入页数
def test_valid_input_order(driver):
    order_page = order_ui(driver)
    result = order_page.valid_input_order()
    assert result