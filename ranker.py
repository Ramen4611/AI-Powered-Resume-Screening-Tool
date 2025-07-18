from ltr_model import load_ltr_model, predict_score
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(resume_data, job_description):
    texts = [job_description] + [r['text'] for r in resume_data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    job_vec = tfidf_matrix[0:1]
    resume_vecs = tfidf_matrix[1:]

    cosine_scores = cosine_similarity(job_vec, resume_vecs)[0]

    model, ltr_vectorizer = load_ltr_model()
    ltr_scores = predict_score([r['text'] for r in resume_data], model, ltr_vectorizer)

    final_scores = [0.7 * c + 0.3 * l for c, l in zip(cosine_scores, ltr_scores)]

    ranked = sorted(zip(resume_data, final_scores), key=lambda x: x[1], reverse=True)
    result = []
    for idx, (data, score) in enumerate(ranked, 1):
        result.append({
            'Rank': idx,
            'File Name': data['filename'],
            'Score': round(score, 3)
        })
    return pd.DataFrame(result)

