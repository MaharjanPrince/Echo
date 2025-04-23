import fitz # type: ignore #PyMuPDF(extracts text from pdf)
def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extracts text from a PDF file's raw binary content.
    Args:
    - pdf_content (bytes): The raw bytes of the uploaded PDF file.
    
    Returns:
    - str: The extracted text from the PDF.
    """
    # Open the PDF from raw bytes
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    
    # Initialize an empty string to store extracted text
    text = ""
    
    # Iterate through all pages and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Get each page
        text += page.get_text("text")  # Extract the text from the page
    
    return text