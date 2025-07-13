import requests
import json
from typing import Dict, Any, Optional
from core.logger import logger
from config.conf import config

class RequestManager:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.get("base_url", "")
        self.timeout = 30
        
        # 设置默认请求头
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "B2C-API-Test/1.0"
        })
        
        # 设置公共参数
        self.common_params = config.get("common_params", {})
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        """
        # 处理完整URL或相对路径
        if not url.startswith(('http://', 'https://')):
            # 如果是相对路径，拼接基础URL
            if url.startswith('/'):
                url = f"{self.base_url}{url}"
            else:
                url = f"{self.base_url}/{url}"
        
        # 设置超时时间
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        # 合并公共参数
        if 'params' in kwargs:
            kwargs['params'].update(self.common_params)
        else:
            kwargs['params'] = self.common_params.copy()
        
        logger.info(f"发送请求: {method} {url}")
        if kwargs.get('data') or kwargs.get('json'):
            logger.debug(f"请求数据: {kwargs.get('data') or kwargs.get('json')}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"响应状态码: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise
    
    def get(self, url: str, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        return self.request("DELETE", url, **kwargs)
    
    def set_token(self, token: str):
        """
        设置认证token
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("已设置认证token")
    
    def clear_token(self):
        """
        清除认证token
        """
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            logger.info("已清除认证token")

# 全局请求管理器实例
request_manager = RequestManager()