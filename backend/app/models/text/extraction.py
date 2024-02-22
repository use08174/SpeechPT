import fitz
from docx import Document
import io

from docx import Document
from PyPDF2 import PdfFileReader

# def extract_text_from_pdf(contents):
#     print("Trying to extract text from PDF...")
#     text = []
#     with fitz.open(stream=io.BytesIO(contents)) as pdf_doc:
#         for page_num in range(pdf_doc.page_count):
#             page = pdf_doc[page_num]
#             text.append(page.get_text())
#     print(f"Extracted text: {text}")
#     return '\n'.join(text)

def extract_text_from_pdf(contents):
    text = []  
    try:
        pdf_doc = fitz.open(stream=io.BytesIO(contents))
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            text.append(page.get_text())
        pdf_doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return {'result': {'error': e}, 'session_id': '49b708e7-064c-4fbe-91f5-1e1336566205'}

    return '\n'.join(text)

def extract_text_from_docx(contents):
    text = [] 
    try:
        doc = Document(io.BytesIO(contents))
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return {'result': {'error': e}, 'session_id': '49b708e7-064c-4fbe-91f5-1e1336566205'}

    return '\n'.join(text)

def extract_text_from_file(file_extension, contents):
    if file_extension == 'pdf':
        return extract_text_from_pdf(contents)
    elif file_extension == 'docx':
        return extract_text_from_docx(contents)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

