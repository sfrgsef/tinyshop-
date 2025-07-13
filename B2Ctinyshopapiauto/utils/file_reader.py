import yaml
import json
import os
from pathlib import Path
from typing import Any, Dict, List
from core.logger import logger

def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    加载YAML文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            logger.info(f"成功加载YAML文件: {file_path}")
            return data
    except Exception as e:
        logger.error(f"加载YAML文件失败: {file_path}, 错误: {e}")
        return {}

def load_json(file_path: str) -> Dict[str, Any]:
    """
    加载JSON文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"成功加载JSON文件: {file_path}")
            return data
    except Exception as e:
        logger.error(f"加载JSON文件失败: {file_path}, 错误: {e}")
        return {}

def load_config(config_path: str = "config/conf.yaml") -> Dict[str, Any]:
    """
    加载配置文件
    """
    return load_yaml(config_path)

def save_yaml(data: Dict[str, Any], file_path: str):
    """
    保存数据到YAML文件
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"成功保存YAML文件: {file_path}")
    except Exception as e:
        logger.error(f"保存YAML文件失败: {file_path}, 错误: {e}")

def save_json(data: Dict[str, Any], file_path: str):
    """
    保存数据到JSON文件
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"成功保存JSON文件: {file_path}")
    except Exception as e:
        logger.error(f"保存JSON文件失败: {file_path}, 错误: {e}")

def get_test_data_files(data_dir: str = "data/testcases") -> List[str]:
    """
    获取测试数据文件列表
    """
    test_files = []
    try:
        for root, dirs, files in os.walk(data_dir):#walk遍历文件夹中的文件，返回三个值，root（文件夹的完整路径，不包括文件），dirs（该文件夹下的子文件夹），files（子文件夹下的所有文件）
            for file in files:
                if file.endswith(('.yaml', '.yml')):
                    test_files.append(os.path.join(root, file))
        logger.info(f"找到 {len(test_files)} 个测试数据文件")
        return test_files
    except Exception as e:
        logger.error(f"获取测试数据文件失败: {e}")
        return []

def ensure_directory_exists(directory: str):
    """
    确保目录存在
    """
    os.makedirs(directory, exist_ok=True)
    logger.debug(f"确保目录存在: {directory}")