import os
import shutil

def copy_en_lproj_contents_only(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        if 'en.lproj' in dirs:
            en_lproj_path = os.path.join(root, 'en.lproj')
            relative_path = os.path.relpath(en_lproj_path, src_dir)
            target_dir = os.path.join(dst_dir, relative_path)
            
            # 如果目标目录不存在，则创建
            os.makedirs(target_dir, exist_ok=True)
            
            # 将en.lproj目录复制到目标目录
            shutil.copytree(en_lproj_path, target_dir, dirs_exist_ok=True)
            print(f"Copied '{en_lproj_path}' to '{target_dir}'")

# 设置源目录和目标目录路径
src_dir = "/Applications/DEVONthink 3.app"
dst_dir = "/Users/saken/Nutstore Files/工作同步/Code/APP-Translate/Programs/DEVONthink/Source"

# 开始复制操作
copy_en_lproj_contents_only(src_dir, dst_dir)
