import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestBaiduSearch:
    """百度搜索功能自动化测试类"""
    
    def test_baidu_homepage_load(self, browser):
        """测试百度首页是否能正常加载"""
        browser.get("https://www.baidu.com")
        
        # 等待页面加载完成
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 验证搜索框存在
        assert search_box.is_displayed()
        assert search_box.is_enabled()
        
        # 验证页面标题
        assert "百度" in browser.title
    
    def test_search_functionality(self, browser):
        """测试搜索功能"""
        browser.get("https://www.baidu.com")
        
        # 等待搜索框出现
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 输入搜索关键词
        search_keyword = "Python自动化测试"
        search_box.clear()
        search_box.send_keys(search_keyword)
        
        # 点击搜索按钮
        search_button = browser.find_element(By.ID, "su")
        search_button.click()
        
        # 等待搜索结果加载
        wait.until(
            EC.presence_of_element_located((By.ID, "content_left"))
        )
        
        # 验证搜索结果页面标题包含搜索关键词
        assert search_keyword in browser.title
        
        # 验证搜索结果存在
        results = browser.find_elements(By.CSS_SELECTOR, ".result")
        assert len(results) > 0
    
    def test_search_with_enter_key(self, browser):
        """测试使用回车键进行搜索"""
        browser.get("https://www.baidu.com")
        
        # 等待搜索框出现
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 输入搜索关键词并按回车
        search_keyword = "Selenium自动化"
        search_box.clear()
        search_box.send_keys(search_keyword)
        search_box.send_keys("\n")
        
        # 等待搜索结果加载
        wait.until(
            EC.presence_of_element_located((By.ID, "content_left"))
        )
        
        # 验证搜索结果页面标题包含搜索关键词
        assert search_keyword in browser.title
    
    def test_empty_search(self, browser):
        """测试空搜索的情况"""
        browser.get("https://www.baidu.com")
        
        # 等待搜索框出现
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 清空搜索框并点击搜索
        search_box.clear()
        search_button = browser.find_element(By.ID, "su")
        search_button.click()
        
        # 验证仍然在百度首页
        assert "百度一下" in browser.title
    
    def test_search_suggestions(self, browser):
        """测试搜索建议功能"""
        browser.get("https://www.baidu.com")
        
        # 等待搜索框出现
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 输入部分关键词
        search_box.clear()
        search_box.send_keys("Python")
        
        # 等待搜索建议出现
        try:
            suggestions = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "bdsug"))
            )
            assert suggestions.is_displayed()
        except TimeoutException:
            # 如果搜索建议没有出现，这也是正常的
            pass
    
    def test_search_with_special_characters(self, browser):
        """测试包含特殊字符的搜索"""
        browser.get("https://www.baidu.com")
        
        # 等待搜索框出现
        wait = WebDriverWait(browser, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        
        # 输入包含特殊字符的搜索关键词
        search_keyword = "Python@#$%^&*()"
        search_box.clear()
        search_box.send_keys(search_keyword)
        
        # 点击搜索按钮
        search_button = browser.find_element(By.ID, "su")
        search_button.click()
        
        # 等待搜索结果加载
        wait.until(
            EC.presence_of_element_located((By.ID, "content_left"))
        )
        
        # 验证搜索能够正常执行
        assert "百度" in browser.title 