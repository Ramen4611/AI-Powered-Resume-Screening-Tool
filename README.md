# 🤖 AI-Powered Resume Screener

A Streamlit-based web app that helps HR teams automatically rank resumes based on how well they match a given job description using Natural Language Processing (NLP).

## 🚀 Features

- 📄 Upload multiple resumes in PDF format
- ✍️ Paste a job description
- 🧠 Uses TF-IDF + Cosine Similarity to rank resumes
- 🟢 Color-coded "Match Quality" scores: Excellent, Fair, Weak
- ⬇️ Download ranked results as a CSV

## 🛠️ Tech Stack

- Python 3.8+
- [Streamlit](https://streamlit.io)
- spaCy
- scikit-learn
- pandas
- PyMuPDF (fitz) or pdfminer

## 📦 Installation

```bash
git clone https://github.com/Ramen4611/AI-Powered Resume Screener Tool.git
cd AI-Powered Resume Screener Tool
pip install -r requirements.txt
streamlit run app.py
