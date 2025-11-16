from pypdf import PdfReader
from modules.chuncker import text_cleaner

def read_pdf(file_path : str) -> dict:
    read = PdfReader(file_path)
    num_pages = len(read.pages)
    all_text = ""
    text = {"metadata" : read.metadata , "num_pages" : num_pages}
    
    for i in range(num_pages):
        text[i] = read.pages[i].extract_text()
        all_text =all_text + read.pages[i].extract_text()

    text["all_text"] = all_text
    
    return text



def clean_text(file_path : str) -> str:
    text = read_pdf(file_path)
    return text_cleaner(text)