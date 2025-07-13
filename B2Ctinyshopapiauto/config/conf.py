import yaml
import os
from pathlib import Path

def load_config(config_path="config/conf.yaml"):
    """
    加载配置文件
    """
    try:
        # 获取项目根目录
        project_root = Path(__file__).parent.parent
        config_file = project_root / config_path
        
        if not config_file.exists():
            # 如果配置文件不存在，返回默认配置
            return get_default_config()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return get_default_config()

def get_default_config():
    """
    返回默认配置
    """
    return {
        "base_url": "http://shop-xo.hctestedu.com/index.php",
        "admin_url": "http://shop-xo.hctestedu.com/admin.php",
        "common_params": {
            "application": "app",
            "application_client_type": "weixin",
            "ajax": "ajax"
        },
        "log_level": "DEBUG",
        "test_account": {
            "username": "huace_tester",
            "password": "huace_tester"
        },
        "allure": {
            "clean_history": True,
            "report_dir": "reports/allure"
        },
        "token_storage": "session"
    }

# 全局配置实例
config = load_config() 