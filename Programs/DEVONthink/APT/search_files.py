# search_files.py
import os
import shutil
import filecmp
import importlib.util

def load_config(software_dir):
    """
    从指定软件目录的APT子目录动态加载配置。
    """
    config_path = os.path.join(software_dir, "APT", "config.py")
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

def get_translated_path(source_path, software_dir, target_language):
    """
    根据源文件路径和目标语言，生成翻译文件的路径。
    """
    relative_path = os.path.relpath(source_path, os.path.join(software_dir, "Source"))
    translated_path = os.path.join(software_dir, "Translated", relative_path.replace("en.lproj", f"{target_language}.lproj"))
    return translated_path

def file_exists_and_mismatch(source_path, target_path):
    """
    检查目标路径的文件是否存在，如果存在，比较其内容是否与源文件不匹配。
    """
    if os.path.exists(target_path):
        return not filecmp.cmp(source_path, target_path, shallow=False)
    return False

def copy_file_to_destination(source_path, destination_dir):
    """
    将文件复制到目标目录，保持原有目录结构。
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
    destination_path = os.path.join(destination_dir, os.path.basename(source_path))
    shutil.copy2(source_path, destination_path)
    print(f"复制文件到：{destination_path}")

def find_and_copy_files(software_dir, file_suffix, target_language):
    source_dir = os.path.join(software_dir, "Source")
    to_translate_dir = os.path.join(software_dir, "ToTranslate")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(file_suffix):
                source_file_path = os.path.join(root, file)
                target_translated_path = get_translated_path(source_file_path, software_dir, target_language)
                
                print(f"\n处理文件：{source_file_path}")
                print(f"翻译文件预期路径：{target_translated_path}")

                if not file_exists_and_mismatch(source_file_path, target_translated_path):
                    target_to_translate_path = os.path.join(to_translate_dir, os.path.relpath(source_file_path, source_dir))
                    if not os.path.exists(target_to_translate_path):
                        print("ToTranslate 目录中未找到文件，进行复制。")
                        copy_file_to_destination(source_file_path, os.path.dirname(target_to_translate_path))
                else:
                    print("文件已翻译，跳过")

def main(software_name, target_language):
    software_dir = os.path.join("Programs", software_name)
    config = load_config(software_dir)
    file_suffix = getattr(config, "FILE_SUFFIX", ".strings")
    find_and_copy_files(software_dir, file_suffix, target_language)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("错误：请指定软件名称和目标语言。")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
