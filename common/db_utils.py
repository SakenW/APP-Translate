import os
import sqlite3
from contextlib import closing

# 获取当前脚本文件所在目录的上一级目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 构建到上一级目录下的database目录中的数据库文件的路径
DATABASE_PATH = os.path.join(base_dir, 'database', 'translation_dict.db')

def get_db_connection():
    """获取数据库连接"""
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(f"数据库连接失败: {e}")
        raise

def check_translation_exists(source_text, software_name, target_language):
    """检查给定源文本、软件名称和目标语言的翻译是否存在"""
    try:
        with closing(get_db_connection()) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute("""
                    SELECT t.translated_text FROM translation t
                    JOIN source_text s ON t.source_text_id = s.id
                    JOIN software sw ON s.software_id = sw.id
                    WHERE s.text = ? AND sw.name = ? AND t.target_language = ?;
                """, (source_text, software_name, target_language))
                result = cur.fetchone()
                if result:
                    print(f"找到翻译：{source_text} -> {result[0]}")
                else:
                    print(f"未找到翻译：{source_text}")
                return result[0] if result else None
    except sqlite3.Error as e:
        print(f"查询翻译失败: {e}")
        return None

def save_translation(source_text, software_name, target_language, translated_text):
    """保存新的翻译"""
    try:
        with closing(get_db_connection()) as conn:
            with closing(conn.cursor()) as cur:
                # 插入或获取software_id
                cur.execute("INSERT OR IGNORE INTO software (name) VALUES (?)", (software_name,))
                cur.execute("SELECT id FROM software WHERE name = ?", (software_name,))
                software_id = cur.fetchone()[0]
                
                # 尝试插入source_text，忽略冲突
                cur.execute("INSERT OR IGNORE INTO source_text (text, software_id) VALUES (?, ?)", (source_text, software_id))
                cur.execute("SELECT id FROM source_text WHERE text = ? AND software_id = ?", (source_text, software_id))
                source_text_id = cur.fetchone()[0]
                
                # 插入或更新翻译
                cur.execute("""
                    INSERT INTO translation (source_text_id, target_language, translated_text) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(source_text_id, target_language) DO UPDATE SET translated_text = excluded.translated_text""",
                            (source_text_id, target_language, translated_text))
                conn.commit()
                print(f"翻译已保存或更新：{source_text} -> {translated_text}")
    except sqlite3.Error as e:
        print(f"保存翻译失败: {e}")

def get_source_texts_by_software(software_name):
    """获取指定软件的所有源文本"""
    try:
        with closing(get_db_connection()) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute("""
                    SELECT s.text FROM source_text s
                    JOIN software sw ON s.software_id = sw.id
                    WHERE sw.name = ?;
                """, (software_name,))
                results = cur.fetchall()
                return [result[0] for result in results]
    except sqlite3.Error as e:
        print(f"获取源文本失败: {e}")
        return []
