# Translate.py

# 导入必要的库
import sqlite3
from googletrans import Translator

# 导入配置
import config.config as config

# 创建翻译器实例
translator = Translator()


def translate_text(text, software_name, target_languages, database_name, source_language='en'):
    # 连接到SQLite数据库
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # 将输入文本转换为小写，以便进行比较
    text_lower = text.lower()

    # 检查源文本是否已在数据库中（忽略大小写）
    cursor.execute("SELECT id FROM source_text WHERE lower(text)=?", (text_lower,))
    row = cursor.fetchone()
    if not row:
        # 如果文本不在数据库中，将其添加到数据库（保留原文本大小写）
        cursor.execute("INSERT INTO source_text (text, software_name) VALUES (?, ?)", (text, software_name))
        conn.commit()
        source_text_id = cursor.lastrowid
    else:
        source_text_id = row[0]

    translations = []
    for target_language in target_languages:
        # 检查翻译是否已存在
        cursor.execute("SELECT translated_text FROM translation WHERE source_text_id=? AND target_language=?", (source_text_id, target_language))
        translated_text_row = cursor.fetchone()  # 获取已翻译文本的行

        if not translated_text_row:
            # 如果没有找到现有翻译，执行翻译操作
            translated = translator.translate(text, src=source_language, dest=target_language)
            translated_text = translated.text
            # 将新翻译添加到返回列表
            translations.append({"target_language": target_language, "translated_text": translated_text, "is_new": True})
            # 将新翻译写入数据库
            cursor.execute("INSERT INTO translation (source_text_id, target_language, translated_text) VALUES (?, ?, ?)", (source_text_id, target_language, translated_text))
            conn.commit()
        else:
            # 如果翻译已存在，从数据库中获取
            translated_text = translated_text_row[0]
            translations.append({"target_language": target_language, "translated_text": translated_text, "is_new": False})

    # 关闭数据库连接
    conn.close()
    return translations
