# log_utils.py

import os
import logging
import logging.config  # 确保这行被正确导入
import functools

from config import LOG_DIR_NAME

# 定义日志目录的完整路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, LOG_DIR_NAME)

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,  # 配置版本

    'disable_existing_loggers': False,  # 不禁用现有的日志记录器

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            # 日志消息格式：时间戳、日志级别、日志记录器名称、消息内容
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',  # 控制台日志记录器的日志级别（DEBUG最详细）
            'class': 'logging.StreamHandler',  # 使用流处理器，将日志消息输出到控制台
            'formatter': 'standard',  # 使用上面定义的'standard'格式
        },

        'file': {
            'level': 'INFO',  # 文件日志记录器的日志级别（INFO较详细）
            'class': 'logging.FileHandler',  # 使用文件处理器，将日志消息输出到文件
            'filename': os.path.join(LOG_DIR, 'app.log'),  # 使用相对路径
            'formatter': 'standard',  # 使用上面定义的'standard'格式
        },
    },

    'loggers': {
        '': {
            'handlers': ['console', 'file'],  # 同时使用控制台和文件处理器
            'level': 'DEBUG',  # 根日志记录器的日志级别
            'propagate': True,  # 允许日志消息传播到更高级别的父日志记录器
        },
    },
}

# 应用日志配置
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# 日志装饰器
def log_print(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        logger.info(message)
        func(*args, **kwargs)
    return wrapper

# 装饰器应用于print_log函数
@log_print
def print_log(*args, **kwargs):
    print(*args, **kwargs)
