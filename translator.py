# translator.py
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

def m2m100_translate(text, src_lang="en", tgt_lang="ko"):
    model_name = "facebook/m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)

    tokenizer.src_lang = src_lang
    encoded = tokenizer(text, return_tensors="pt")
    
    generated_tokens = model.generate(
        **encoded, 
        forced_bos_token_id=tokenizer.get_lang_id(tgt_lang)
    )
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text
