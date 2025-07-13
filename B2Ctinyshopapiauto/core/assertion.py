from core.logger import logger

class Assertion:
    @staticmethod #装饰器，通常用一不需要访问和修改的类
    def assert_status_code(response, expected_status_code):
        """
        断言响应状态码
        """
        actual_status_code = response.status_code
        assert actual_status_code == expected_status_code, \
            f"状态码断言失败: 期望 {expected_status_code}, 实际 {actual_status_code}"#如果失败就直接返回，后面不执行
        logger.info(f"状态码断言成功: {actual_status_code}")
    
    @staticmethod
    def assert_response_code(response_data, expected_code):
        """
        断言API响应码
        """
        actual_code = response_data.get("code")
        assert actual_code == expected_code, \
            f"响应码断言失败: 期望 {expected_code}, 实际 {actual_code}"
        logger.info(f"响应码断言成功: {actual_code}")
    
    @staticmethod
    def assert_message(response_data, expected_message):
        """
        断言响应消息
        """
        actual_message = response_data.get("message", "")#不存在message就返回空
        assert expected_message in actual_message, \
            f"消息断言失败: 期望包含 '{expected_message}', 实际 '{actual_message}'"
        logger.info(f"消息断言成功: {actual_message}")
    
    @staticmethod
    def assert_field_exists(response_data, field_path):
        """
        断言字段存在
        """
        fields = field_path.split(".")
        current = response_data
        
        for field in fields:
            assert field in current, f"字段不存在: {field_path}"
            current = current[field]
        
        logger.info(f"字段存在断言成功: {field_path}")
    
    @staticmethod
    def assert_field_value(response_data, field_path, expected_value):
        """
        断言字段值
        """
        fields = field_path.split(".")
        current = response_data
        
        for field in fields:
            assert field in current, f"字段不存在: {field_path}"
            current = current[field]
        
        actual_value = current
        assert actual_value == expected_value, \
            f"字段值断言失败: 期望 {expected_value}, 实际 {actual_value}"
        logger.info(f"字段值断言成功: {field_path} = {actual_value}")
    
    @staticmethod
    def assert_field_not_empty(response_data, field_path):
        """
        断言字段不为空
        """
        fields = field_path.split(".")#split(".")通过.分割field_path
        current = response_data
        
        for field in fields:
            assert field in current, f"字段不存在: {field_path}"
            current = current[field]
        
        actual_value = current
        assert actual_value, f"字段为空: {field_path}"
        logger.info(f"字段非空断言成功: {field_path}")
    
    @staticmethod
    def assert_list_length(response_data, field_path, expected_length):
        """
        断言列表长度
        """
        fields = field_path.split(".")
        current = response_data
        
        for field in fields:
            assert field in current, f"字段不存在: {field_path}"
            current = current[field]
        
        actual_length = len(current) if isinstance(current, list) else 0
        assert actual_length == expected_length, \
            f"列表长度断言失败: 期望 {expected_length}, 实际 {actual_length}"
        logger.info(f"列表长度断言成功: {field_path} = {actual_length}")
    
    @staticmethod
    def assert_response_structure(response_data, expected_structure):
        """
        断言响应结构
        """
        def check_structure(data, structure):
            if isinstance(structure, dict):
                assert isinstance(data, dict), f"期望字典类型, 实际 {type(data)}"
                for key, value in structure.items():
                    assert key in data, f"缺少字段: {key}"
                    check_structure(data[key], value)
            elif isinstance(structure, list):
                assert isinstance(data, list), f"期望列表类型, 实际 {type(data)}"
                if data and structure:
                    check_structure(data[0], structure[0])
        
        check_structure(response_data, expected_structure)
        logger.info("响应结构断言成功")
    
    @staticmethod
    def assert_json_schema(response_data, schema):
        """
        断言JSON Schema (简化版)
        """
        # 这里可以实现更复杂的JSON Schema验证
        # 目前只做基本的类型检查
        def validate_schema(data, schema):
            if schema.get("type") == "object":
                assert isinstance(data, dict), f"期望对象类型"
                for required_field in schema.get("required", []):
                    assert required_field in data, f"缺少必需字段: {required_field}"
            elif schema.get("type") == "array":
                assert isinstance(data, list), f"期望数组类型"
        
        validate_schema(response_data, schema)
        logger.info("JSON Schema断言成功")