# main.py
from scraper import get_all_paper_links, get_paper_details
from translator import m2m100_translate

def main():
    base_url = 'https://huggingface.co/papers'
    paper_links = get_all_paper_links(base_url)
    print("Paper links:", paper_links)
    
    for link in paper_links:
        paper_data = get_paper_details(link)
        print("\nPaper detail data:", paper_data)
        
        # abstract 번역 (영어 -> 한국어)
        translated_abstract = m2m100_translate(paper_data['abstract'], src_lang="en", tgt_lang="ko")
        print("Translated abstract:", translated_abstract)

if __name__ == '__main__':
    main()
