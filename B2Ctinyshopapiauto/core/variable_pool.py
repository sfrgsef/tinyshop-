from typing import Any, Dict, Optional
from core.logger import logger

class VariablePool:
    def __init__(self):
        self._variables = {}
    
    def set(self, key: str, value: Any):
        """
        设置变量
        """
        self._variables[key] = value
        logger.info(f"设置变量: {key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取变量
        """
        value = self._variables.get(key, default)
        if value is not None:
            logger.debug(f"获取变量: {key} = {value}")
        return value
    
    def delete(self, key: str):
        """
        删除变量
        """
        if key in self._variables:
            del self._variables[key]
            logger.info(f"删除变量: {key}")
    
    def clear(self):
        """
        清空所有变量
        """
        self._variables.clear()
        logger.info("清空所有变量")
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有变量
        """
        return self._variables.copy()
    
    def exists(self, key: str) -> bool:
        """
        检查变量是否存在
        """
        return key in self._variables
    
    def update(self, variables: Dict[str, Any]):
        """
        批量更新变量
        """
        self._variables.update(variables)
        logger.info(f"批量更新变量: {list(variables.keys())}")
    
    def extract_and_set(self, response_data: dict, extraction_rules: Dict[str, str]):
        """
        从响应数据中提取并设置变量
        """
        from core.jsonpath_extractor import JsonPathExtractor
        
        for var_name, jsonpath_expr in extraction_rules.items():
            value = JsonPathExtractor.extract(response_data, jsonpath_expr)
            if value is not None:
                self.set(var_name, value)
            else:
                logger.warning(f"提取变量失败: {var_name} <- {jsonpath_expr}")

# 全局变量池实例
variable_pool = VariablePool()