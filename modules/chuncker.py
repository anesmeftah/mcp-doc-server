import re
from ftfy import fix_text
from utils.utils import find_nth
from collections import Counter

def text_cleaner(text_dict : dict) -> str:

    text = text_dict['text']
    num_pages = text_dict['num_pages']
    clean_text = fix_text(text)
    clean_text = re.sub(r"-\n","",clean_text)
    clean_text = re.sub(r"\n{2,}", "\n\n", clean_text)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    repeated_lines = get_repeated_line(text_dict , num_pages)
    for line in repeated_lines:
        clean_text = re.sub(re.escape(line), "", clean_text)
    
    
    return clean_text



def get_repeated_line(text_dict : dict , num_pages : int) -> list:
    repeated_line = []
    lines_per_page = [0] * num_pages
    for i in range(num_pages):
        first_line = find_nth(text_dict[i] , "\n" , 1)
        second_line = find_nth(text_dict[i] , "\n" , 2)
        third_line = find_nth(text_dict[i] , "\n" , 3)
        lines = [text_dict[i][:first_line] , text_dict[i][first_line:second_line] , text_dict[i][second_line:third_line]]
        lines_per_page[i] = lines

        percentage_dict = cal_per(lines_per_page , num_pages)
        result = []
        for line , percentage in percentage_dict.items():
            if percentage > 0.8:
                result.append(line)
    return result


def cal_per(liste : list , num_pages : int) -> dict:
    """calculate the percentage of presence of each sentence"""
    presence_counter = Counter()

    for page in liste:
        unique_lines = set(page)
        for line in unique_lines:
            presence_counter[line] += 1

    result = {}
    for line , count in presence_counter.items(): 
        result[line] = (count / num_pages) 
    return result
