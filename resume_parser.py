import PyPDF2
import os

# Function to extract text from a single PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Function to extract text from all PDFs in the 'resumes/' folder
def get_all_resumes(folder_path='resumes'):
    resumes = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            resumes[filename] = text
    return resumes
