from typing import Any, List, Optional
from core.logger import logger
from jsonpath_ng import parse

class JsonPathExtractor:
    @staticmethod
    def extract(response_data: dict, jsonpath_expr: str) -> Optional[Any]:
        """
        使用JSONPath提取数据
        """
        try:
            expr = parse(jsonpath_expr)
            matches = [match.value for match in expr.find(response_data)]
            if matches:
                logger.info(f"JSONPath提取成功: {jsonpath_expr} -> {matches[0]}")
                return matches[0] if len(matches) == 1 else matches
            else:
                logger.warning(f"JSONPath未找到匹配: {jsonpath_expr}")
                return None
        except Exception as e:
            logger.error(f"JSONPath提取失败: {jsonpath_expr}, 错误: {e}")
            return None
    
    @staticmethod
    def extract_all(response_data: dict, jsonpath_expr: str) -> List[Any]:
        """
        使用JSONPath提取所有匹配的数据
        """
        try:
            expr = parse(jsonpath_expr)
            matches = [match.value for match in expr.find(response_data)]
            if matches:
                logger.info(f"JSONPath提取成功: {jsonpath_expr} -> {len(matches)} 个结果")
                return matches
            else:
                logger.warning(f"JSONPath未找到匹配: {jsonpath_expr}")
                return []
        except Exception as e:
            logger.error(f"JSONPath提取失败: {jsonpath_expr}, 错误: {e}")
            return []
    
    @staticmethod
    def extract_field(response_data: dict, field_path: str) -> Optional[Any]:
        """
        使用点分隔的字段路径提取数据
        """
        try:
            fields = field_path.split(".")
            current = response_data
            
            for field in fields:
                if isinstance(current, dict) and field in current:
                    current = current[field]
                else:
                    logger.warning(f"字段路径不存在: {field_path}")
                    return None
            
            logger.info(f"字段提取成功: {field_path} -> {current}")
            return current
        except Exception as e:
            logger.error(f"字段提取失败: {field_path}, 错误: {e}")
            return None
    
    @staticmethod
    def extract_by_condition(response_data: dict, condition: dict) -> Optional[Any]:
        """
        根据条件提取数据
        """
        try:
            # 支持多种条件类型
            if "jsonpath" in condition:
                return JsonPathExtractor.extract(response_data, condition["jsonpath"])
            elif "field" in condition:
                return JsonPathExtractor.extract_field(response_data, condition["field"])
            elif "index" in condition:
                # 提取数组中的指定索引
                field_path = condition.get("field", "")
                index = condition["index"]
                data = JsonPathExtractor.extract_field(response_data, field_path)
                if isinstance(data, list) and 0 <= index < len(data):
                    return data[index]
                else:
                    logger.warning(f"索引提取失败: {field_path}[{index}]")
                    return None
            else:
                logger.error(f"不支持的条件类型: {condition}")
                return None
        except Exception as e:
            logger.error(f"条件提取失败: {condition}, 错误: {e}")
            return None