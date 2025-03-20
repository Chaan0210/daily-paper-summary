from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("papers.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    papers = conn.execute("SELECT * FROM papers").fetchall()
    conn.close()
    return render_template("index.html", papers=papers)

if __name__ == "__main__":
    app.run(debug=True)
