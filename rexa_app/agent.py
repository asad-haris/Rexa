import streamlit as st
import pandas as pd
from resume_parser import get_all_resumes
from matcher import calculate_similarity
import os
from prompts import resume_feedback_prompt
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="Rexa - AI Resume Screener", layout="centered")
st.title("🧠 Rexa - AI Resume Screening & Ranking System")

# Upload job description
st.subheader("📄 Upload Job Description (Text File)")
job_desc_file = st.file_uploader("Upload .txt file", type=['txt'])

# Upload resumes
st.subheader("📁 Upload Resumes (PDFs)")
resume_files = st.file_uploader("Upload one or more .pdf resumes", type=['pdf'], accept_multiple_files=True)

if job_desc_file and resume_files:
    job_description = job_desc_file.read().decode('utf-8')

    # Create resumes folder if it doesn't exist
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

    # Save uploaded resumes
    for file in resume_files:
        with open(f"resumes/{file.name}", "wb") as f:
            f.write(file.read())

    # Extract resume text
    resumes = get_all_resumes("resumes")

    # Calculate match scores
    scores = calculate_similarity(resumes, job_description)

    # Display ranked resumes
    st.subheader("📊 Ranked Resumes")
    df = pd.DataFrame(scores.items(), columns=["Resume", "Match Score (%)"])
    df = df.sort_values(by="Match Score (%)", ascending=False)
    st.dataframe(df)

    # Allow CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download Results", data=csv, file_name="resume_ranking.csv", mime="text/csv")

    # AI Feedback Section
    st.subheader("💬 AI Feedback for Each Resume")
    for filename, resume_text in resumes.items():
        try:
            prompt_text = f"{resume_feedback_prompt}\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"
            feedback = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Change to "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are an AI recruiter."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.7
            )
            st.write(f"**{filename}**")
            st.write(feedback.choices[0].message["content"])
        except Exception as e:
            st.error(f"Error generating feedback for {filename}: {e}")