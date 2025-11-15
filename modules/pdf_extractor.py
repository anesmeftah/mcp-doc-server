from pypdf import PdfReader

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