from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to calculate similarity between resumes and job description
def calculate_similarity(resumes, job_description):
    scores = {}
    for filename, resume_text in resumes.items():
        documents = [resume_text, job_description]
        tfidf = TfidfVectorizer().fit_transform(documents)
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        scores[filename] = round(score * 100, 2)  # Convert to percentage
    return scores
