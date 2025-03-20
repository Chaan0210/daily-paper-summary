# date_handler.py
import threading
from scraper import get_all_paper_links, get_paper_details
from translator import translate
from summarizer import extract_text_from_pdf, summarize_text
from db_func import paper_exists, save_paper

scraping_threads = {}

def process_date(date_str):
    print(f"[{date_str}] process_date started.")
    base_url = f"https://huggingface.co/papers/date/{date_str}"
    paper_links = get_all_paper_links(base_url)
    print(f"[{date_str}] paper links:", paper_links)

    for link in paper_links:
        paper_data = get_paper_details(link)
        paper_data['date'] = date_str

        if paper_exists(paper_data['pdf_link']):
            print(f"[{date_str}] Already in DB, skipping: {paper_data['pdf_link']}")
            continue

        translated_abstract = translate(paper_data['abstract'], src_lang="English", tgt_lang="Korean")
        pdf_text = extract_text_from_pdf(paper_data['pdf_link'])
        pdf_summary = summarize_text(pdf_text, tgt_lang="Korean")

        paper_record = {
            'title': paper_data['title'],
            'abstract': paper_data['abstract'],
            'pdf_link': paper_data['pdf_link'],
            'translated_abstract': translated_abstract,
            'summary': pdf_summary,
            'num_vote': paper_data['num_vote'],
            'date': date_str
        }
        save_paper(paper_record)
        print(f"[{date_str}] Paper saved: {paper_data['pdf_link']}")

    print(f"[{date_str}] Scraping complete.")

    scraping_threads.pop(date_str, None)
    print(f"[{date_str}] Removed from scraping_threads.")


def start_scraping_async(date_str):
    if date_str in scraping_threads:
        print(f"[{date_str}] Scraping is already in progress.")
        return

    print(f"[{date_str}] Starting scraping in a new thread.")
    t = threading.Thread(target=process_date, args=(date_str,))
    scraping_threads[date_str] = t
    t.start()