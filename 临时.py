# replace_percent_sign_verbose.py
import os
import sys

# 确保db_utils.py所在的目录被添加到模块搜索路径中
sys.path.append(os.path.dirname(__file__))

from common.db_utils import get_db_connection

def fetch_translations_to_replace():
    """获取所有包含全角百分比符号的翻译文本"""
    select_query = """
    SELECT id, translated_text
    FROM translation
    WHERE translated_text LIKE '%％%'
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def replace_full_width_percent_sign():
    """替换所有全角百分比符号为半角百分比符号，并逐行打印"""
    translations = fetch_translations_to_replace()
    if not translations:
        print("没有找到需要替换的文本。")
        return
    
    update_query = """
    UPDATE translation
    SET translated_text = ?
    WHERE id = ?
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for row in translations:
            original_text = row[1]
            replaced_text = original_text.replace('％', '%')
            cursor.execute(update_query, (replaced_text, row[0]))
            print(f"原文本: {original_text}\n替换后: {replaced_text}\n")
        conn.commit()
        print(f"已成功替换所有全角百分比符号。")
    except Exception as e:
        print(f"替换全角百分比符号时发生错误: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    replace_full_width_percent_sign()
