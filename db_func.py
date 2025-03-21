# db_func.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("papers.db")
    conn.row_factory = sqlite3.Row
    return conn

def paper_exists(pdf_link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers WHERE pdf_link = ?", (pdf_link,))
    row = cursor.fetchone()
    conn.close()
    return row

def save_paper(paper):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO papers (title, abstract, pdf_link, translated_abstract, summary, num_vote, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            paper['title'], 
            paper['abstract'], 
            paper['pdf_link'], 
            paper['translated_abstract'], 
            paper['summary'], 
            paper['num_vote'],
            paper['date']
        ))
        conn.commit()
        print("[DB] Commit successful for:", paper['pdf_link'])
    except Exception as e:
        print("[DB] ERROR saving paper:", e)
    finally:
        conn.close()