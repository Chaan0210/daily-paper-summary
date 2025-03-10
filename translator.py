# translator.py
import re
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

def m2m100_translate(text, src_lang="en", tgt_lang="ko"):
    model_name = "facebook/m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)

    text = " ".join(text.split())
    
    tokenizer.src_lang = src_lang
    encoded = tokenizer(text, return_tensors="pt", truncation=True)

    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.get_lang_id(tgt_lang),
        max_length=512,
        num_beams=5,
        early_stopping=True
    )
    translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    return translated_text

def m2m100_translate_full(text, src_lang="en", tgt_lang="ko"):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    translated_sentences = []
    for sentence in sentences:
        if sentence.strip():
            translation = m2m100_translate(sentence, src_lang, tgt_lang)
            translated_sentences.append(translation)
    return " ".join(translated_sentences)
