import sys
import os

def parse_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        sys.exit(1)
        
    # Attempt to import pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except ImportError:
        pass

    # Attempt to import pdfplumber
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except ImportError:
        pass

    # Attempt to import PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except ImportError:
        pass

    print("Error: No PDF parsing libraries found (pypdf, pdfplumber, PyPDF2). Please install one using 'pip install pypdf'.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_pdf.py <path_to_pdf>", file=sys.stderr)
        sys.exit(1)
    pdf_path = sys.argv[1]
    extracted_text = parse_pdf(pdf_path)
    print(extracted_text)
