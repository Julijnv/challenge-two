import pdfplumber

# This function reads the specified PDF file and returns all the extracted text as a single string.
def extract_text_from_pdf(pdf_path: str) -> str:
    
    with pdfplumber.open(pdf_path) as pdf:
        text_pages = []
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)
        return "\n".join(text_pages)


#raw_text = extract_text_from_pdf("C:/Users/jnv77/Documents/Astrafy/challenge-two/papers/paper1.pdf")
#print(raw_text)