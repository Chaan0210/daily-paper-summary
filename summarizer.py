# summarizer.py
import requests
from io import BytesIO
import PyPDF2
import re
from transformers import pipeline

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

def summarize_text(pdf_text):
    prompt = pdf_text + "\n\n이 글을 한국어로 요약하고 정리해."
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", trust_remote_code=True)
    result = pipe(prompt)
    
    return result[0]['generated_text']
