import streamlit as st
import pandas as pd
from resume_parser import get_all_resumes
from matcher import calculate_similarity
import os

# Streamlit UI
st.set_page_config(page_title="Rexa - AI Resume Screener", layout="centered")
st.title("🧠 Rexa - AI Resume Screening & Ranking System")

# Upload Job Description
st.subheader("📄 Upload Job Description (Text File)")
job_desc_file = st.file_uploader("Upload .txt file", type=['txt'])

# Upload Resumes
st.subheader("📁 Upload Resumes (PDFs)")
resume_files = st.file_uploader("Upload one or more .pdf resumes", type=['pdf'], accept_multiple_files=True)

# Process Inputs
if job_desc_file and resume_files:
    job_description = job_desc_file.read().decode('utf-8')

    # Create 'resumes' folder if not exists
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

    # Save uploaded resumes
    for file in resume_files:
        with open(f"resumes/{file.name}", "wb") as f:
            f.write(file.read())

    # Extract text from resumes
    resumes = get_all_resumes("resumes")

    # Calculate similarity
    scores = calculate_similarity(resumes, job_description)

    # Display results
    st.subheader("📊 Ranked Resumes")
    df = pd.DataFrame(scores.items(), columns=["Resume", "Match Score (%)"])
    df = df.sort_values(by="Match Score (%)", ascending=False)
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Results", data=csv, file_name="resume_ranking.csv", mime="text/csv")
