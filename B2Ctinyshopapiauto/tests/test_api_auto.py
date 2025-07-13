import pytest
import json
import allure
from typing import Dict, Any, List, Union
from core.logger import logger
from core.request_manager import request_manager
from core.assertion import Assertion
from core.variable_pool import variable_pool
from core.jsonpath_extractor import JsonPathExtractor
from utils.file_reader import load_yaml, get_test_data_files
from utils.data_processor import DataProcessor
from utils.allure_utils import (
    AllureDecorator, AllureReporter, 
    get_test_category, get_test_severity, create_allure_description,
    AllureRawWriter
)

class TestAPIAuto:
    """API自动化测试类"""
    
    def setup_class(self):
        """测试类初始化"""
        logger.info("开始API自动化测试")
        #遍历测试用例文件yaml文件的路径
        self.test_data_files = get_test_data_files()
        self.allure_writer = AllureRawWriter()

    #整个测试类的所有测试用例执行完毕后进行资源清理
    def teardown_class(self):
        """测试类清理"""
        logger.info("API自动化测试完成")
    
    @pytest.mark.parametrize("test_file", get_test_data_files())
    @pytest.mark.api_test
    @allure.epic("B2C商城API自动化测试")
    @allure.feature("API接口测试")
    def test_api_cases(self, test_file):
        """执行测试文件中的所有测试用例"""
        # 获取测试分类
        test_category = get_test_category(test_file)
        
        # 添加Allure装饰器
        allure.dynamic.feature(test_category)
        allure.dynamic.description(f"执行测试文件: {test_file}")
        
        logger.info(f"开始执行测试文件: {test_file}")
        
        # 加载测试数据
        test_cases = load_yaml(test_file)
        if not test_cases:
            logger.warning(f"测试文件为空: {test_file}")
            return
        
        # 处理测试用例 - 支持列表和字典两种格式，isinstance判断数据是否时期望的格式
        if isinstance(test_cases, list):
            # 列表格式：每个测试用例是一个列表项
            for i, case_data in enumerate(test_cases):#enumerate将数据读取为索引+value的格式
                if isinstance(case_data, dict):
                    case_name = case_data.get("name", f"test_case_{i}")#找不到name就返回商城的索引
                    self._execute_test_case(case_name, case_data, test_file)
                else:
                    logger.warning(f"跳过无效的测试用例: {case_data}")
        elif isinstance(test_cases, dict):
            # 字典格式：每个测试用例是一个键值对
            for case_name, case_data in test_cases.items():#遍历字典以元组的形式呈现，元组（键名：值）
                if isinstance(case_data, dict):
                    self._execute_test_case(case_name, case_data, test_file)
                else:
                    logger.warning(f"跳过无效的测试用例: {case_name}")
        else:
            logger.error(f"不支持的测试数据格式: {type(test_cases)}")
    
    def _execute_test_case(self, case_name: str, case_data: Dict[str, Any], test_file: str):
        """执行单个测试用例"""
        # 获取测试用例的严重程度
        severity_level = get_test_severity(case_name)
        
        # 创建Allure描述
        description = create_allure_description(case_data)
        
        # 添加Allure装饰器
        allure.dynamic.story(case_name)
        allure.dynamic.severity(severity_level)
        allure.dynamic.description(description)
        
        logger.info(f"执行测试用例: {case_name}")
        
        try:
            # 处理动态数据
            allure.step("处理动态数据")
            processed_data = DataProcessor.process_dynamic_data(case_data)
            
            # 解析变量
            allure.step("解析变量")
            resolved_data = DataProcessor.resolve_variables(processed_data, variable_pool)
            
            # 提取请求信息
            allure.step("提取请求信息")
            request_data = resolved_data.get("request", {})
            method = request_data.get("method", "GET")
            url = request_data.get("url", "")
            headers = request_data.get("headers", {})
            json_data = request_data.get("json", {})
            params = request_data.get("params", {})
            
            # 添加请求信息到Allure报告
            AllureReporter.add_request_info(method, url, headers, json_data, params)
            
            # 发送请求
            allure.step(f"发送 {method} 请求到 {url}")
            response = request_manager.request(method, url, headers=headers, json=json_data, params=params)
            
            # 添加响应信息到Allure报告
            AllureReporter.add_response_info(
                response.status_code, 
                dict(response.headers), 
                response.text
            )
            
            # 解析响应
            allure.step("解析响应数据")
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"text": response.text}
            
            # 添加响应数据到Allure报告
            AllureReporter.add_json_data(response_data, "Response Data")
            
            # 执行断言
            allure.step("执行断言验证")
            validation_rules = resolved_data.get("validate", [])
            validation_results = []
            
            for rule in validation_rules:
                for assertion_type, assertion_data in rule.items():
                    try:
                        if assertion_type == "eq":
                            field, expected_value = assertion_data
                            Assertion.assert_field_value(response_data, field, expected_value)
                            validation_results.append({
                                "type": "eq",
                                "field": field,
                                "expected": expected_value,
                                "status": "PASS"
                            })
                        elif assertion_type == "contains":
                            field, expected_value = assertion_data
                            Assertion.assert_message(response_data, expected_value)
                            validation_results.append({
                                "type": "contains",
                                "field": field,
                                "expected": expected_value,
                                "status": "PASS"
                            })
                        elif assertion_type == "exists":
                            field = assertion_data
                            Assertion.assert_field_exists(response_data, field)
                            validation_results.append({
                                "type": "exists",
                                "field": field,
                                "status": "PASS"
                            })
                        elif assertion_type == "status_code":
                            Assertion.assert_status_code(response, assertion_data)
                            validation_results.append({
                                "type": "status_code",
                                "expected": assertion_data,
                                "actual": response.status_code,
                                "status": "PASS"
                            })
                        else:
                            logger.warning(f"不支持的断言类型: {assertion_type}")
                            validation_results.append({
                                "type": assertion_type,
                                "status": "SKIP"
                            })
                    except Exception as e:
                        logger.error(f"断言失败: {assertion_type} - {e}")
                        validation_results.append({
                            "type": assertion_type,
                            "error": str(e),
                            "status": "FAIL"
                        })
                        raise
            
            # 添加验证信息到Allure报告
            AllureReporter.add_validation_info(validation_rules, validation_results)
            
            # 提取变量
            allure.step("提取变量")
            extract_rules = resolved_data.get("extract", {})
            extracted_values = {}
            
            for var_name, jsonpath_expr in extract_rules.items():
                value = JsonPathExtractor.extract(response_data, jsonpath_expr)
                if value is not None:
                    variable_pool.set(var_name, value)
                    extracted_values[var_name] = value
                    logger.info(f"提取变量: {var_name} = {value}")
                else:
                    logger.warning(f"提取变量失败: {var_name} <- {jsonpath_expr}")
                    extracted_values[var_name] = None
            
            # 添加提取信息到Allure报告
            AllureReporter.add_extraction_info(extract_rules, extracted_values)
            
            # 记录日志内容
            log_str = f"请求: {method} {url}\n请求头: {headers}\n请求体: {json_data}\n响应: {response.text}\n断言: {validation_results}\n提取: {extracted_values}"
            # 写入Allure原始结果
            self.allure_writer.add_test_result(
                name=case_name,
                status="passed",
                request=request_data,
                response=response_data,
                validations=validation_results,
                logs=log_str,
                test_file=test_file
            )
            logger.info(f"测试用例执行成功: {case_name}")
            
        except Exception as e:
            logger.error(f"测试用例执行失败: {case_name}, 错误: {e}")
            self.allure_writer.add_test_result(
                name=case_name,
                status="failed",
                request=request_data if 'request_data' in locals() else {},
                response=response_data if 'response_data' in locals() else {},
                validations=validation_results if 'validation_results' in locals() else [],
                logs=log_str if 'log_str' in locals() else '',
                error=str(e),
                test_file=test_file
            )
            # 添加错误信息到Allure报告
            AllureReporter.add_error_info(e, f"测试用例: {case_name}")
            raise

# 测试钩子函数
def pytest_configure(config):
    """pytest配置钩子"""
    logger.info("pytest配置完成")

def pytest_collection_modifyitems(items):
    """测试用例收集修改钩子"""
    for item in items:
        # 为所有测试用例添加标记
        item.add_marker(pytest.mark.api_test)