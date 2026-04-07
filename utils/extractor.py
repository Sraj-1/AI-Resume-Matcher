import pdfplumber
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from PDF (works with Streamlit file uploader or normal file).
    """
    text = ""

    try:
        # IMPORTANT: Reset file pointer (fixes empty output issue)
        uploaded_file.seek(0)

        with pdfplumber.open(uploaded_file) as pdf:
            if not pdf.pages:
                logging.warning("No pages found in PDF.")
                return ""

            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()

                    if page_text:
                        # Clean weird bullet characters
                        page_text = page_text.replace("", "").replace("\uf0b7", "")
    
                        text += page_text + "\n"
                    else:
                        logging.warning(f"No text on page {i+1}")

                except Exception as page_error:
                    logging.error(f"Error on page {i+1}: {page_error}")

        return text.strip()

    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return ""