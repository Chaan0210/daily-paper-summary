# scraper.py
import requests
from bs4 import BeautifulSoup

def get_all_paper_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paper_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/papers/') and len(href.split('/')) == 3 and '#community' not in href:
            paper_links.append("https://huggingface.co" + href)
    return list(set(paper_links))

def get_paper_details(paper_url):
    response = requests.get(paper_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').get_text(strip=True)
    title = title.replace("\n", " ")

    abstract_elem = soup.find('p', class_='text-gray-600')
    abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""
    abstract = abstract.replace("\n", " ")

    paper_id = paper_url.split('/papers/')[1].split('#')[0]
    pdf_link = "https://arxiv.org/pdf/" + paper_id

    return {'title': title, 'abstract': abstract, 'pdf_link': pdf_link}
