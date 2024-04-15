import os

# 数据库名称，默认从环境变量获取，没有则使用默认值
DATABASE_NAME = os.getenv('DATABASE_NAME', "translation_dict.db")

# 日志目录名称
LOG_DIR_NAME = 'logs'

# 目标翻译语言
TARGET_LANGUAGES = [
    "zh-CN",  # 简体中文
    # "en-US",  # 美国英语
    # "ja-JP",  # 日本
    # "ko-KR",  # 韩国
    # 在此添加更多语言...
]

# 应用程序列表
APPLICATIONS = [
    "DEVONthink",
    "Hazel",
    # "AnotherApp",
    # 在此添加更多应用...
]