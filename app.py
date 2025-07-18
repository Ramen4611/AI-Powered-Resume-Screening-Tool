import streamlit as st
from parser import extract_text_from_pdf
from ranker import rank_resumes
from utils import get_download_link
import re

# --- Page setup ---
st.set_page_config(page_title="Resume Screener", layout="centered")

# --- Enhanced CSS Styling with Background ---
st.markdown("""
    <style>
        body {
            background-image: url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }
        .main {
            background: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
        }
        h1 {
            color: #2C3E50;
            text-align: center;
            font-size: 2.8rem;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 12px 24px;
            transition: all 0.3s ease;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #16a085;
        }
        .stTextArea textarea, .stFileUploader {
            background-color: #fefefe;
            border: 1px solid #ddd;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.95rem;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<h1>🤖 AI-Powered Resume Screener</h1>", unsafe_allow_html=True)
st.markdown('<div class="main">', unsafe_allow_html=True)

# --- Collapsible About Section ---
with st.expander("ℹ️ About this app"):
    st.write("""
        This AI-powered resume screening tool helps HR teams quickly identify top candidates.
        It uses Natural Language Processing (NLP) with TF-IDF and cosine similarity to rank resumes
        based on how well they match a given job description. Upload multiple PDF resumes,
        paste a job description, and get an instant, ranked list with match quality indicators.

        **Built with:** Python, spaCy, pandas, Streamlit
    """)

# --- Job Description Input ---
st.subheader("📄 Paste the Job Description")
job_desc = st.text_area("Job description", height=200)

# Preprocess job description
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

job_desc_cleaned = clean_text(job_desc)

# --- Upload Resumes ---
st.subheader("📎 Upload PDF Resumes")
uploaded_files = st.file_uploader("Upload one or more resumes", type="pdf", accept_multiple_files=True)

# --- Run Analysis ---
if st.button("🔍 Analyze Resumes"):
    if not job_desc or not uploaded_files:
        st.warning("Please upload at least one resume and paste a job description.")
    else:
        data = []
        with st.spinner("Processing resumes..."):
            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                if not text.strip():
                    st.warning(f"⚠️ Could not extract text from {file.name}.")
                    continue
                cleaned_text = clean_text(text)
                data.append({'filename': file.name, 'text': cleaned_text})

            if not data:
                st.error("No valid resumes to analyze.")
            else:
                result_df = rank_resumes(data, job_desc_cleaned)
                st.success("✅ Ranking complete!")

                def label_score(score):
                    if score > 0.7:
                        return "🟢 Excellent"
                    elif score > 0.4:
                        return "🟡 Fair"
                    else:
                        return "🔴 Weak"

                result_df["Match Quality"] = result_df["Score"].apply(label_score)

                st.dataframe(result_df.style.applymap(
                    lambda val: 'background-color: #d6f5d6' if isinstance(val, str) and 'Excellent' in val 
                    else 'background-color: #fff9cc' if 'Fair' in val 
                    else 'background-color: #ffd6cc' if 'Weak' in val else '', subset=['Match Quality']
                ))

                st.markdown(get_download_link(result_df), unsafe_allow_html=True)

# --- Footer ---
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer'>Built with ❤️ using Python, NLP, and Streamlit</div>",
    unsafe_allow_html=True
)