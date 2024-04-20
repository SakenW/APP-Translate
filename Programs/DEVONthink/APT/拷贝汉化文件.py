import os
import shutil

def copy_back_to_app(src_dir, app_dir):
    for root, dirs, files in os.walk(src_dir):
        # 计算目标路径
        relative_path = os.path.relpath(root, src_dir)
        target_dir = os.path.join(app_dir, relative_path)
        
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(target_dir, file)
            
            # 直接复制并替换目标文件
            shutil.copy2(src_file_path, dst_file_path)
            print(f"Copied '{src_file_path}' to '{dst_file_path}'")
        
        # 可选：复制目录（如果需要复制空目录或特定的目录结构）

# 设置源目录和目标目录路径
src_dir = "/Users/saken/Nutstore Files/工作同步/Code/APP-Translate/Programs/DEVONthink/Translated"
app_dir = "/Applications/DEVONthink 3.app"

# 开始复制操作
copy_back_to_app(src_dir, app_dir)
