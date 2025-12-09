# matcher.py – Calculates similarity between resumes and job descriptions using OpenAI embeddings
import os
import openai
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get embeddings from OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")  # Clean newlines
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return np.array(response['data'][0]['embedding'])

# Function to calculate similarity using cosine similarity on embeddings
def calculate_similarity(resumes, job_description):
    scores = {}

    # Get job description embedding once
    job_desc_embedding = get_embedding(job_description)

    for filename, resume_text in resumes.items():
        try:
            resume_embedding = get_embedding(resume_text)
            # Cosine similarity calculation
            similarity = np.dot(resume_embedding, job_desc_embedding) / (
                np.linalg.norm(resume_embedding) * np.linalg.norm(job_desc_embedding)
            )
            scores[filename] = round(similarity * 100, 2)  # Percentage
        except Exception as e:
            scores[filename] = f"Error: {e}"

    return scores
