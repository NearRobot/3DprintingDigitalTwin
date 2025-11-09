"""
日志管理模块

提供统一的日志记录接口，支持控制台和文件输出。
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    日志管理器类
    
    封装 Python logging 模块，提供便捷的日志记录功能。
    
    属性:
        logger (logging.Logger): Python 标准日志记录器
        log_dir (Path): 日志文件目录
    """
    
    def __init__(
        self,
        name: str = "control-sim",
        level: str = "INFO",
        log_dir: Optional[str] = None,
        console_output: bool = True,
        file_output: bool = True,
    ):
        """
        初始化日志管理器
        
        参数:
            name: 日志记录器名称
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: 日志文件保存目录
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除已有的处理器
        self.logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 添加控制台处理器
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # 添加文件处理器
        if file_output:
            if log_dir is None:
                log_dir = "logs"
            
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建带时间戳的日志文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.log_dir / f"{name}_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """记录 DEBUG 级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录 INFO 级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录 WARNING 级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录 ERROR 级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录 CRITICAL 级别日志"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """记录异常信息（包含堆栈跟踪）"""
        self.logger.exception(message)


# 全局日志记录器实例
_global_logger: Optional[Logger] = None


def get_logger(
    name: str = "control-sim",
    level: str = "INFO",
    log_dir: Optional[str] = None,
) -> Logger:
    """
    获取日志记录器实例
    
    如果全局日志记录器不存在，则创建新的实例。
    
    参数:
        name: 日志记录器名称
        level: 日志级别
        log_dir: 日志文件保存目录
    
    返回:
        Logger 实例
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = Logger(name=name, level=level, log_dir=log_dir)
    
    return _global_logger


def setup_logger(
    name: str = "control-sim",
    level: str = "INFO",
    log_dir: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True,
) -> Logger:
    """
    设置全局日志记录器
    
    参数:
        name: 日志记录器名称
        level: 日志级别
        log_dir: 日志文件保存目录
        console_output: 是否输出到控制台
        file_output: 是否输出到文件
    
    返回:
        Logger 实例
    """
    global _global_logger
    
    _global_logger = Logger(
        name=name,
        level=level,
        log_dir=log_dir,
        console_output=console_output,
        file_output=file_output,
    )
    
    return _global_logger
