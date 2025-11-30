import logging,os
from datetime import datetime

class Log():
    def __init__(self) -> None:
        # 解决windows系统在cmd运行日志显示异常问题
        os.system('')
        
        # 创建logs目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 设置日志文件名
        log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
        
        # 创建logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('\033[33m[%(asctime)s][%(levelname)s]:\033[0m%(message)s')
        console_handler.setFormatter(console_formatter)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
        file_handler.setFormatter(file_formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # 设置urllib3日志级别
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    
    def info(self,msg) -> None:
        self.logger.info(msg)

    def debug(self,msg) -> None:
        self.logger.debug(msg)

    def error(self,msg) -> None:
        self.logger.error(msg)
    
    def warning(self,msg) -> None:
        self.logger.warning(msg)

    def critical(self,msg) -> None:
        self.logger.critical(msg)
    