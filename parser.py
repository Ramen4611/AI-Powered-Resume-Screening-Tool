import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]
    return list(set(keywords))
