import fitz  # PyMuPDF

def extract_text(resume_file):
    text = ""
    with fitz.open(stream=resume_file.read(), filetype="pdf") as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
    return text