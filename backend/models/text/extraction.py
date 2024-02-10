import fitz
from docx import Document
import io

def extract_text_from_pdf(contents):
    text = []
    with fitz.open(stream=io.BytesIO(contents)) as pdf_doc:
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            text.append(page.get_text())

    return '\n'.join(text)

def extract_text_from_docx(contents):
    doc = Document(io.BytesIO(contents))
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text_from_file(file_extension, contents):
    if file_extension == 'pdf':
        return extract_text_from_pdf(contents)
    elif file_extension == 'docx':
        return extract_text_from_docx(contents)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

