from pypdf import PdfReader

def read_pdf(file_path : str) -> dict:
    read = PdfReader(file_path)
    num_pages = len(read.pages)
    all_text = ""
    
    for i in range(num_pages):
        all_text =all_text + read.pages[i].extract_text()
    
    text = {"metadata" : read.metadata,
            "text" : all_text
        }
    return text