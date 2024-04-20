import os
import chardet
from common.db_utils import check_translation_exists

def remove_empty_directories(path, stop_dir):
    """
    递归删除空目录，直到指定的停止目录。
    :param path: 当前检查的目录路径
    :param stop_dir: 停止删除的目录名称
    """
    if not os.path.isdir(path) or os.path.basename(path) == stop_dir:
        return
    if not os.listdir(path):
        os.rmdir(path)
        print(f"删除空目录：{path}")
        remove_empty_directories(os.path.dirname(path), stop_dir)
    else:
        # 如果目录不为空，检查每个子目录是否为空
        for dir in os.listdir(path):
            full_dir_path = os.path.join(path, dir)
            if os.path.isdir(full_dir_path):
                remove_empty_directories(full_dir_path, stop_dir)

def save_translation_for_software(software_name, target_language):
    print("开始执行保存翻译的函数。")
    base_dir = os.path.dirname(os.path.abspath(__file__)).split('Programs')[0]
    to_translate_path = os.path.join(base_dir, "Programs", software_name, "ToTranslate")
    translated_path = os.path.join(base_dir, "Programs", software_name, "Translated")

    for root, dirs, files in os.walk(to_translate_path):
        for file in files:
            if file == ".DS_Store":
                continue

            original_file_path = os.path.join(root, file)
            print(f"处理文件：{original_file_path}")

            with open(original_file_path, 'rb') as rawdata:
                encoding = chardet.detect(rawdata.read())['encoding']

            translated_file_dir = root.replace("ToTranslate", "Translated").replace("en.lproj", f"{target_language}.lproj")
            translated_file_path = os.path.join(translated_file_dir, file)
            os.makedirs(translated_file_dir, exist_ok=True)

            with open(original_file_path, 'r', encoding=encoding) as original, open(translated_file_path, 'w', encoding='utf-8') as translated:
                for line in original:
                    if '=' not in line:
                        translated.write(line)
                        continue
                    
                    key, value = line.split('=', 1)
                    # 移除值两端的空格、引号和分号
                    value = value.strip().strip('"').rstrip(';"') 
                    translation = check_translation_exists(value, software_name, target_language)
                    if translation:
                        line = f'{key.strip()} = "{translation}";\n'
                    translated.write(line)

            print(f"完成处理文件并生成：{translated_file_path}")
            
            # 删除原始文件
            os.remove(original_file_path)
            print(f"删除原始文件：{original_file_path}")

            # 删除所有空的上层目录，直到`ToTranslate`目录
            remove_empty_directories(os.path.dirname(original_file_path), "ToTranslate")

    print("完成保存翻译的函数。")
