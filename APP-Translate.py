#APP-Translate.py
import os
import sys
import importlib.util
import getpass

# 从common包导入db_utils模块
from common import db_utils

# 如果log_utils模块中有logger对象，则这样导入
from common.log_utils import logger

# 从common.Translate包导入Googletrans模块中的GoogleTranslate类
from common.Translate.Googletrans import GoogleTranslate

from common.Translate.Openaitrans import OpenAITranslate

# 导入APPLICATIONS和TARGET_LANGUAGES常量˚
from config import APPLICATIONS, TARGET_LANGUAGES

# 导入模块选择功能
def choose_translation_module():
    modules = ["Googletrans", "Openaitrans"]
    print("请选择翻译模块：")
    for index, module in enumerate(modules, start=1):
        print(f"{index}. {module}")
    choice = int(input("请输入选择的翻译模块编号：")) - 1
    return modules[choice]

def get_api_key_if_needed(module_name):
    if module_name == "Openaitrans":
        return getpass.getpass("请输入OpenAI API密钥：")
    return None

def load_module(module_name, path):
    """动态加载模块"""
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def choose_from_list(prompt, items):
    """让用户从列表中选择一个项"""
    print(prompt)
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")
    choice = int(input("请选择一个选项（输入序号）: ")) - 1
    return items[choice]

def main():
    # 选择翻译模块
    translation_module_name = choose_translation_module()
    api_key = get_api_key_if_needed(translation_module_name)
    
    # 动态导入选定的翻译模块
    if translation_module_name == "Googletrans":
        from common.Translate.Googletrans import GoogleTranslate as Translator
    elif translation_module_name == "Openaitrans":
        from common.Translate.Openaitrans import OpenAITranslate as Translator

    translator = Translator(api_key) if api_key else Translator()

    software_name = choose_from_list("请选择要翻译的软件：", APPLICATIONS)
    logger.info(f"选中的软件：{software_name}")
    target_language = choose_from_list("请选择目标翻译语言：", TARGET_LANGUAGES)
    logger.info(f"目标翻译语言：{target_language}")

    search_files_path = f"Programs/{software_name}/APT/search_files.py"
    file_parser_path = f"Programs/{software_name}/APT/file_parser.py"
    save_translation_path = f"Programs/{software_name}/APT/save_translation.py"

    logger.info("开始动态加载模块...")
    search_files_module = load_module("search_files", search_files_path)
    file_parser_module = load_module("file_parser", file_parser_path)
    save_translation_module = load_module("save_translation", save_translation_path)

    translator = GoogleTranslate()

    logger.info("开始搜索待翻译文件...")
    search_files_module.main(software_name, target_language)
    
    to_translate_dir = os.path.join("Programs", software_name, "ToTranslate")
    logger.info(f"待翻译文件目录：{to_translate_dir}")
    for root, dirs, files in os.walk(to_translate_dir):
        for file in files:
            file_path = os.path.join(root, file)
            logger.info(f"处理文件：{file_path}")
            translations = file_parser_module.parse_strings_file(file_path)
            for key, value in translations.items():
                logger.info(f"检查翻译是否存在：{key}: {value}")
                existing_translation = db_utils.check_translation_exists(value, software_name, target_language)
                if not existing_translation:
                    logger.info(f"翻译不存在，开始翻译：{value}")
                    translated_text = translator.translate(value, target_language, software_name)
                    if translated_text:
                        db_utils.save_translation(value, software_name, target_language, translated_text)
                        logger.info(f"翻译并保存了新的翻译：{key}: {translated_text}")
                    else:
                        logger.error(f"无法翻译文本：{value}")
                else:
                    logger.info(f"已存在翻译：{key}: {existing_translation}")
    
    # 新添加的写入翻译模块调用
    logger.info("开始将翻译写入新文件...")
    save_translation_module.save_translation_for_software(software_name, target_language)

if __name__ == "__main__":
    main()
