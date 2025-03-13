# main.py
from scraper import get_all_paper_links, get_paper_details
from translator import m2m100_translate_full
from summarizer import extract_text_from_pdf, summarize_text

def main():
    base_url = 'https://huggingface.co/papers'
    paper_links = get_all_paper_links(base_url)
    print("Paper links:", paper_links)
    
    for link in paper_links:
        paper_data = get_paper_details(link)
        print("\nPaper detail data:", paper_data)
        
        translated_abstract = m2m100_translate_full(paper_data['abstract'], src_lang="en", tgt_lang="ko")
        print("Translated abstract:", translated_abstract)
        
        pdf_text = extract_text_from_pdf(paper_data['pdf_link'])
        pdf_summary = summarize_text(pdf_text)
        print("PDF Summary:", pdf_summary)

if __name__ == '__main__':
    main()
