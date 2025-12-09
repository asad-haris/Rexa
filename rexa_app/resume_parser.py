import os
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

# Path to tesseract (only needed if it's not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    text = ""

    # 1. Try extracting normal text
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    # 2. If no text found, use OCR on images
    if not text.strip():
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.strip()

def get_all_resumes(folder_path='resumes'):
    resumes = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            resumes[filename] = text
    return resumes
