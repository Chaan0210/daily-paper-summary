# db_setup.py
import sqlite3

def create_db():
    conn = sqlite3.connect("papers.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            abstract TEXT,
            pdf_link TEXT UNIQUE,
            translated_abstract TEXT,
            summary TEXT,
            num_vote TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database and table created (or already exist).")
