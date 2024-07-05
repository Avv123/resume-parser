import PyPDF2


def extract_text(resume_file):
    # Read the uploaded resume file
    pdf_reader = PyPDF2.PdfReader(resume_file)
    
    # Extract text from each page in the PDF
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Return the extracted text
    return text