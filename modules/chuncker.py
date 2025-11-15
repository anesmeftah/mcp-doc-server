import re
from ftfy import fix_text
from utils.utils import find_nth

def text_cleaner(text_dict : dict) -> str:

    text = text_dict['text']
    num_pages = text_dict['num_pages']
    clean_text = fix_text(text)
    clean_text = re.sub(r"-\n","",clean_text)
    clean_text = re.sub(r"\n{2,}", "\n\n", clean_text)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    clean_text = get_repeated_line(text_dict , num_pages)
    return clean_text



def get_repeated_line(text_dict : dict , num_pages : int) -> list:
    repeated_line = []
    lines_per_page = [0] * num_pages
    for i in range(num_pages):
        lines = 
        lines_per_page[i] = text_dict[i][]