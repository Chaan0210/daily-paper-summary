# app.py
from flask import Flask, render_template, jsonify
import markdown
import datetime
from date_handler import start_scraping_async
from db_func import get_db_connection

app = Flask(__name__)

def convert_markdown(text):
    return markdown.markdown(text or "")

@app.route("/")
def index():
    today_str = datetime.date.today().isoformat()
    return papers_by_date(today_str)

@app.route("/papers/<date_str>")
def papers_by_date(date_str):
    start_scraping_async(date_str)

    return render_template("index.html", current_date=date_str)

@app.route("/api/papers/<date_str>")
def api_papers_by_date(date_str):
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT * FROM papers
        WHERE date = ?
        ORDER BY CAST(num_vote AS INTEGER) DESC
    """, (date_str,)).fetchall()
    conn.close()

    papers = []
    for row in rows:
        d = dict(row)
        d["summary_md"] = convert_markdown(d["summary"])
        d["translated_abstract_md"] = convert_markdown(d["translated_abstract"])
        papers.append(d)
    return jsonify(papers)

@app.route("/api/date-nav/<date_str>")
def api_date_nav(date_str):
    current_date = datetime.date.fromisoformat(date_str)
    prev_date = current_date - datetime.timedelta(days=1)
    next_date = current_date + datetime.timedelta(days=1)

    today = datetime.date.today()
    can_go_next = (next_date <= today)

    return jsonify({
        "prev_date": prev_date.isoformat(),
        "next_date": next_date.isoformat(),
        "can_go_next": can_go_next
    })

if __name__ == "__main__":
    app.run(debug=True)
