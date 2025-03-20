# translator.py
import requests

def ollama_generate(prompt, model="exaone3.5"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "applicaion/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['response']


def translate(text, src_lang="en", tgt_lang="ko"):
    prompt = f"Translate the following text from {src_lang} to {tgt_lang}:\n\n{text}\n\nTranslated text in {tgt_lang}:"
    return ollama_generate(prompt, model="exaone3.5")

def translate_full(text, src_lang="en", tgt_lang="ko"):
    return translate(text, src_lang, tgt_lang)
