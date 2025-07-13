import re
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List
from core.logger import logger
from config.conf import config

class DataProcessor:
    @staticmethod
    def resolve_variables(data: Any, variable_pool) -> Any:
        """
        解析数据中的变量占位符
        """
        if isinstance(data, dict):
            return {k: DataProcessor.resolve_variables(v, variable_pool) for k, v in data.items()}
        elif isinstance(data, list):
            return [DataProcessor.resolve_variables(item, variable_pool) for item in data]
        elif isinstance(data, str):
            # 处理 {{variable}} 语法
            matches = re.findall(r"\{\{(.*?)\}\}", data)
            for match in matches:
                var_value = DataProcessor._get_variable_value(match, variable_pool)
                if var_value is not None:
                    data = data.replace(f"{{{{{match}}}}}", str(var_value))
            return data
        else:
            return data
    
    @staticmethod
    def _get_variable_value(var_path: str, variable_pool) -> Any:
        """
        获取变量值，支持配置变量和变量池变量
        """
        # 首先检查是否是配置变量
        if var_path.startswith("config."):#startswith判断字符是否以（）开头
            # 处理配置变量，如 config.test_account.username
            config_path = var_path.replace("config.", "")#replace把字符串里特定的子串替换成别的字符串
            return DataProcessor._get_nested_value(config, config_path)
        else:
            # 从变量池获取
            return variable_pool.get(var_path)
    
    @staticmethod
    def _get_nested_value(data: Any, path: str) -> Any:
        """
        从嵌套字典中获取值，支持点分隔的路径
        """
        try:
            keys = path.split(".")
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    logger.warning(f"配置路径不存在: {path}")
                    return None
            return current
        except Exception as e:
            logger.error(f"获取配置值失败: {path}, 错误: {e}")
            return None
    
    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """
        生成随机字符串
        """
        #random.choices用于从序列（如列表、元组）中进行带权重的随机选择，可以重复选择同一元素，string.ascii_letters包含大小写字母，string.digits包含数字
        #''.join链接符为空
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_email() -> str:
        """
        生成随机邮箱
        """
        username = DataProcessor.generate_random_string(8)
        domain = random.choice(['example.com', 'test.com', 'demo.com'])
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_phone() -> str:
        """
        生成随机手机号
        """
        prefix = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139'])
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"
    
    @staticmethod
    def generate_timestamp(offset_days: int = 0) -> str:
        """
        生成时间戳
        """
        dt = datetime.now() + timedelta(days=offset_days)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def generate_date(offset_days: int = 0) -> str:
        """
        生成日期
        """
        dt = datetime.now() + timedelta(days=offset_days)
        return dt.strftime("%Y-%m-%d")
    
    @staticmethod
    def process_dynamic_data(data: Any) -> Any:#data: Any类型注解，表示可以为任意类型
        """
        处理动态数据生成
        """
        #提取列表或者字典的值
        if isinstance(data, dict):
            return {k: DataProcessor.process_dynamic_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DataProcessor.process_dynamic_data(item) for item in data]

        elif isinstance(data, str):
            # 处理动态数据占位符
            if data == "{{random_string}}":
                return DataProcessor.generate_random_string()
            elif data == "{{random_email}}":
                return DataProcessor.generate_random_email()
            elif data == "{{random_phone}}":
                return DataProcessor.generate_random_phone()
            elif data == "{{timestamp}}":
                return DataProcessor.generate_timestamp()
            elif data == "{{date}}":
                return DataProcessor.generate_date()
            elif data.startswith("{{random_string(") and data.endswith(")}}"):#检查是否以{{random_string(开头，以)}}结尾
                # 提取长度参数
                length_str = data[16:-2]  # 去掉 "{{random_string(" 和 ")}"
                try:
                    length = int(length_str)
                    return DataProcessor.generate_random_string(length)
                except ValueError:
                    logger.warning(f"无效的随机字符串长度: {length_str}")
                    return DataProcessor.generate_random_string()
            else:
                return data
        else:
            return data
    
    @staticmethod
    def merge_data(base_data: Dict[str, Any], override_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并数据，override_data会覆盖base_data中的相同键
        """
        result = base_data.copy()
        result.update(override_data)
        return result
    
    @staticmethod
    def filter_data(data: Dict[str, Any], include_keys: List[str] = None, exclude_keys: List[str] = None) -> Dict[str, Any]:
        """
        过滤数据
        """
        if include_keys:
            return {k: v for k, v in data.items() if k in include_keys}
        elif exclude_keys:
            return {k: v for k, v in data.items() if k not in exclude_keys}
        else:
            return data
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        验证必需字段
        """
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            logger.error(f"缺少必需字段: {missing_fields}")
            return False
        return True