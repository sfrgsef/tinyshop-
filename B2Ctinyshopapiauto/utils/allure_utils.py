import subprocess
import os
import shutil
from pathlib import Path
from core.logger import logger
import platform
import allure
import json
from datetime import datetime
from typing import Dict, Any, Optional
import uuid
import time

def get_allure_cmd():
    if platform.system() == "Windows":
        return os.path.join("D:\\allure\\allure-2.34.1\\bin", "allure.bat")
    else:
        return "allure"

def generate_allure_report(raw_results_dir: str, report_dir: str):
    """
    生成Allure报告
    """
    try:
        # 确保报告目录存在
        os.makedirs(report_dir, exist_ok=True)
        
        # 检查allure命令是否可用
        if not is_allure_available():
            logger.warning("Allure命令不可用，跳过报告生成")
            return False
        
        # 生成报告
        cmd = [get_allure_cmd(), "generate", raw_results_dir, "-o", report_dir, "--clean"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Allure报告生成成功: {report_dir}")
            return True
        else:
            logger.error(f"Allure报告生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"生成Allure报告时出错: {e}")
        return False

def is_allure_available() -> bool:
    """
    检查Allure是否可用
    """
    try:
        result = subprocess.run([get_allure_cmd(), "--version"], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def open_allure_report(report_dir: str):
    """
    打开Allure报告
    """
    try:
        if not is_allure_available():
            logger.warning("Allure命令不可用，无法打开报告")
            return False
        
        cmd = [get_allure_cmd(), "open", report_dir]
        subprocess.Popen(cmd)
        logger.info(f"已打开Allure报告: {report_dir}")
        return True
    except Exception as e:
        logger.error(f"打开Allure报告失败: {e}")
        return False

def clean_allure_results(results_dir: str):
    """
    清理Allure结果目录
    """
    try:
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)
            logger.info(f"已清理Allure结果目录: {results_dir}")
    except Exception as e:
        logger.error(f"清理Allure结果目录失败: {e}")

def create_allure_environment(env_data: dict, output_dir: str = "reports/allure_raw"):
    """
    创建Allure环境配置文件
    """
    try:
        env_file = os.path.join(output_dir, "environment.properties")
        os.makedirs(output_dir, exist_ok=True)
        
        with open(env_file, 'w', encoding='utf-8') as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")
        
        logger.info(f"已创建Allure环境配置: {env_file}")
    except Exception as e:
        logger.error(f"创建Allure环境配置失败: {e}")

def setup_allure_environment():
    """
    设置Allure环境配置
    """
    from config.conf import config
    
    env_data = {
        "Base_URL": config.get("base_url", ""),
        "Environment": "Test",
        "Framework": "pytest",
        "Python_Version": "3.x",
        "Test_Account": config.get("test_account", {}).get("username", ""),
        "Application": config.get("common_params", {}).get("application", ""),
        "Client_Type": config.get("common_params", {}).get("application_client_type", "")
    }
    
    create_allure_environment(env_data)

# 新增的Allure装饰器和工具函数
class AllureDecorator:
    """Allure装饰器工具类"""
    
    @staticmethod
    def feature(feature_name: str):
        """功能特性装饰器"""
        return allure.feature(feature_name)
    
    @staticmethod
    def story(story_name: str):
        """用户故事装饰器"""
        return allure.story(story_name)
    
    @staticmethod
    def severity(severity_level: str):
        """严重程度装饰器"""
        return allure.severity(severity_level)
    
    @staticmethod
    def epic(epic_name: str):
        """史诗装饰器"""
        return allure.epic(epic_name)
    
    @staticmethod
    def description(desc: str):
        """描述装饰器"""
        return allure.description(desc)
    
    @staticmethod
    def link(url: str, name: str = ""):
        """链接装饰器"""
        return allure.link(url, name)
    
    @staticmethod
    def issue(issue_id: str, url: str = ""):
        """问题装饰器"""
        return allure.issue(issue_id, url)
    
    @staticmethod
    def testcase(testcase_id: str, url: str = ""):
        """测试用例装饰器"""
        return allure.testcase(testcase_id, url)

class AllureReporter:
    """Allure报告工具类"""
    
    @staticmethod
    def add_request_info(method: str, url: str, headers: Optional[Dict] = None, 
                        data: Any = None, params: Optional[Dict] = None):
        """添加请求信息到Allure报告"""
        request_info = {
            "Method": method,
            "URL": url,
            "Headers": headers if headers else {},
            "Data": data,
            "Params": params if params else {}
        }
        
        allure.attach(
            json.dumps(request_info, indent=2, ensure_ascii=False),
            "Request Information",
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def add_response_info(status_code: int, headers: Dict, body: Any):
        """添加响应信息到Allure报告"""
        response_info = {
            "Status Code": status_code,
            "Headers": headers,
            "Body": body
        }
        
        allure.attach(
            json.dumps(response_info, indent=2, ensure_ascii=False),
            "Response Information",
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def add_validation_info(validation_rules: list, validation_results: list):
        """添加验证信息到Allure报告"""
        validation_info = {
            "Validation Rules": validation_rules,
            "Validation Results": validation_results
        }
        
        allure.attach(
            json.dumps(validation_info, indent=2, ensure_ascii=False),
            "Validation Information",
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def add_extraction_info(extraction_rules: Dict, extracted_values: Dict):
        """添加提取信息到Allure报告"""
        extraction_info = {
            "Extraction Rules": extraction_rules,
            "Extracted Values": extracted_values
        }
        
        allure.attach(
            json.dumps(extraction_info, indent=2, ensure_ascii=False),
            "Extraction Information",
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def add_error_info(error: Exception, context: str = ""):
        """添加错误信息到Allure报告"""
        error_info = {
            "Error Type": type(error).__name__,
            "Error Message": str(error),
            "Context": context,
            "Timestamp": datetime.now().isoformat()
        }
        
        allure.attach(
            json.dumps(error_info, indent=2, ensure_ascii=False),
            "Error Information",
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def add_screenshot(screenshot_path: str, name: str = "Screenshot"):
        """添加截图到Allure报告"""
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name, allure.attachment_type.PNG)
    
    @staticmethod
    def add_log(log_content: str, name: str = "Log"):
        """添加日志到Allure报告"""
        allure.attach(log_content, name, allure.attachment_type.TEXT)
    
    @staticmethod
    def add_json_data(data: Any, name: str = "JSON Data"):
        """添加JSON数据到Allure报告"""
        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False),
            name,
            allure.attachment_type.JSON
        )

class AllureRawWriter:
    def __init__(self, results_dir='reports/allure_raw'):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def add_test_result(self, name, status, request, response, validations, logs, error=None, test_file=None):
        test_id = str(uuid.uuid4())
        result_file = self.results_dir / f'{test_id}-result.json'
        req_file = self.results_dir / f'{test_id}_request.json'
        resp_file = self.results_dir / f'{test_id}_response.json'
        with open(req_file, 'w', encoding='utf-8') as f:
            json.dump(request, f, ensure_ascii=False, indent=2)
        with open(resp_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        attachments = [
            {"name": "请求数据", "type": "application/json", "source": req_file.name},
            {"name": "响应数据", "type": "application/json", "source": resp_file.name},
        ]
        if logs:
            log_file = self.results_dir / f'{test_id}_log.txt'
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(logs)
            attachments.append({"name": "日志", "type": "text/plain", "source": log_file.name})
        if validations:
            val_file = self.results_dir / f'{test_id}_validations.json'
            with open(val_file, 'w', encoding='utf-8') as f:
                json.dump(validations, f, ensure_ascii=False, indent=2)
            attachments.append({"name": "断言结果", "type": "application/json", "source": val_file.name})
        # 分类分组：parentSuite=API自动化测试, suite=模块名, subSuite=YAML文件名
        labels = [
            {"name": "parentSuite", "value": "API自动化测试"}
        ]
        if test_file:
            module = os.path.basename(os.path.dirname(test_file))
            yamlfile = os.path.splitext(os.path.basename(test_file))[0]
            labels.append({"name": "suite", "value": module})
            labels.append({"name": "subSuite", "value": yamlfile})
            labels.append({"name": "feature", "value": module})
        else:
            labels.append({"name": "suite", "value": "default"})
        result = {
            "name": name,
            "status": status,
            "stage": "finished",
            "start": int(time.time() * 1000),
            "stop": int(time.time() * 1000),
            "uuid": test_id,
            "fullName": name,
            "labels": labels,
            "attachments": attachments,
            "description": error or "",
        }
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

def get_test_category(file_path: str) -> str:
    """根据文件路径获取测试分类"""
    if "auth" in file_path:
        return "认证模块"
    elif "goods" in file_path:
        return "商品模块"
    elif "order" in file_path:
        return "订单模块"
    elif "user" in file_path:
        return "用户模块"
    elif "cart" in file_path:
        return "购物车模块"
    elif "payment" in file_path:
        return "支付模块"
    elif "address" in file_path:
        return "地址模块"
    else:
        return "其他模块"

def get_test_severity(case_name: str) -> str:
    """根据测试用例名称判断严重程度"""
    critical_keywords = ["登录", "支付", "下单", "注册"]
    high_keywords = ["详情", "搜索", "列表", "查询"]
    medium_keywords = ["更新", "修改", "编辑"]
    
    for keyword in critical_keywords:
        if keyword in case_name:
            return "critical"
    
    for keyword in high_keywords:
        if keyword in case_name:
            return "high"
    
    for keyword in medium_keywords:
        if keyword in case_name:
            return "medium"
    
    return "low"

def create_allure_description(case_data: Dict[str, Any]) -> str:
    """创建Allure描述"""
    description = case_data.get("description", "")
    name = case_data.get("name", "")
    
    desc_parts = []
    if name:
        desc_parts.append(f"测试用例: {name}")
    if description:
        desc_parts.append(f"描述: {description}")
    
    # 添加请求信息
    request_data = case_data.get("request", {})
    if request_data:
        method = request_data.get("method", "GET")
        url = request_data.get("url", "")
        desc_parts.append(f"请求: {method} {url}")
    
    return "\n".join(desc_parts)