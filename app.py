from flask import Flask, render_template
import sqlite3
import markdown

app = Flask(__name__)

def convert_markdown(text):
    return markdown.markdown(text)

def get_db_connection():
    conn = sqlite3.connect("papers.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM papers ORDER BY CAST(num_vote AS INTEGER) DESC").fetchall()
    conn.close()

    papers = [dict(row) for row in rows]

    for paper in papers:
        paper["summary_md"] = convert_markdown(paper["summary"])
        paper["translated_abstract_md"] = convert_markdown(paper["translated_abstract"])

    return render_template("index.html", papers=papers)

if __name__ == "__main__":
    app.run(debug=True)
