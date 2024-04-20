import sqlite3

def create_tables():
    db_path = "/Users/saken/Nutstore Files/工作同步/Code/APP-Translate/database/translation_dict.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS software (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );''')

    c.execute('''CREATE TABLE IF NOT EXISTS source_text (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    software_id INTEGER,
                    FOREIGN KEY (software_id) REFERENCES software(id)
                );''')

    c.execute('''CREATE TABLE IF NOT EXISTS translation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text_id INTEGER NOT NULL,
                    target_language TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    FOREIGN KEY (source_text_id) REFERENCES source_text(id),
                    UNIQUE(source_text_id, target_language)
                );''')

    conn.commit()
    conn.close()

create_tables()
