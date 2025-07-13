import logging
import os
from datetime import datetime
from config.conf import config


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:# 若实例不存在，创建新实例
            cls._instance = super().__new__(cls) #super在子类中调用父类的函数
            cls._instance.init_logger()# 初始化日志配置
        return cls._instance

    def init_logger(self):
        self.logger = logging.getLogger("api_test")# 创建名为"api_test"的日志器
        self.logger.setLevel(config.get("log_level", "INFO")) # 设置日志级别（默认INFO）

        # 创建日志目录
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)#exist_ok目录存在就不会报错

        # 文件日志格式
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s" #创建时间，名为"api_test"的日志器，日志级别，日志内容
        )

        # 控制台日志格式
        console_formatter = logging.Formatter(
            "%(levelname)s - %(message)s" #日志级别，日志内容
        )

        # 日志文件命名格式
        log_file = os.path.join(
            log_dir,
            f"api_test_{datetime.now().strftime('%Y%m%d')}.log"
        )
        #创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(file_formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


# 全局日志实例
logger = Logger()