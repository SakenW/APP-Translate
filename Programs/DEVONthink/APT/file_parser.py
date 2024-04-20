# file_parser.py
import os
import codecs
from common.log_utils import logger  # 确保正确导入日志工具

def parse_strings_file(file_path):
    try:
        translations = {}
        with codecs.open(file_path, 'r', encoding='utf-16-le') as file:
            first_char = file.read(1)  # 读取第一个字符
            if first_char != '\ufeff':  # 检查是否为 BOM
                file.seek(0)  # 如果不是 BOM，回到文件开头
            for line in file:
                if "=" in line and ";" in line:
                    key, value = line.split('=', 1)
                    key = key.strip().strip('"')
                    value = value.strip().split(';')[0].strip('"')
                    translations[key] = value
        return translations
    except UnicodeDecodeError as e:
        logger.error(f"无法解码文件 {file_path}: {e}")
    except FileNotFoundError as e:
        logger.error(f"文件未找到 {file_path}: {e}")
    return {}

# 示例调用
if __name__ == "__main__":
    file_path = 'Programs/DEVONthink/ToTranslate/PlugIns/DTScannerPlugin.bundle/Contents/Resources/en.lproj/Localizable.strings'
    translations = parse_strings_file(file_path)
    if translations:
        logger.info(f"提取的键值对: {translations}")
    else:
        logger.info("没有提取到任何键值对。")