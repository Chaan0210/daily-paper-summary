# summarizer.py
import requests
from io import BytesIO
import PyPDF2
import re
from translator import ollama_generate

def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    pdf_file = BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            match = re.search(r'(?i)References\s*\n\s*\[\d+\]', page_text)
            if match:
                full_text += page_text[:match.start()]
                break
            else:
                full_text += page_text + "\n"
    return full_text

def summarize_text(pdf_text, tgt_lang="ko"):
    prompt = pdf_text + f"\n\nSummarize this article in {tgt_lang} in great detail."
    return ollama_generate(prompt, model="exaone3.5")
