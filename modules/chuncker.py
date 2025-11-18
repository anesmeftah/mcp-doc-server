import re
from ftfy import fix_text
from utils.utils import find_nth , get_fin
from collections import Counter

def text_cleaner(text_dict : dict) -> str:
    """ Cleaning text before chunking"""
    text = text_dict['all_text']
    num_pages = text_dict['num_pages']
    print("BEFORE CLEANING\n\n\n" ,text[:10000] , "\n\n\n")
    
    cleaned_pages = [clean_page(text_dict[i]) for i in range(num_pages)]
    repeated_lines = get_repeated_line(text_dict , num_pages)
    for i in range(num_pages):

        for line in repeated_lines:
            cleaned_pages[i] = re.sub(re.escape(line), "", cleaned_pages[i])
    print("AFTER CLEANING\n\n\n" , cleaned_pages[0])
    return cleaned_pages

def clean_page(page: str) -> str:

    clean_text = re.sub(r"-\n", "", page)
    clean_text = re.sub(r"\n{2,}", "\n\n", clean_text)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    clean_text = fix_text(clean_text)
    clean_text = re.sub(r"(?im)^\s*(?:page|p\.?)\s*\d+\s*(?:of\s*\d+|/\s*\d+)?\s*$", "", clean_text)
    clean_text = re.sub(r"(?m)^[\s\-\u2010-\u2015]*\d+\s*(?:/\s*\d+)?[\s\-\u2010-\u2015]*$", "", clean_text)
    clean_text = re.sub(r"(?m)^[\s\-\u2010-\u2015]*[ivxlcdmIVXLCDM]+\s*$", "", clean_text)
    clean_text = re.sub(r"(?m)^\s*\d+\s*$", "", clean_text)

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


def structure_segmentation(pages : list) -> dict:
    sections = []
    header_pattern = r"^(Chapter\s+\d+|Section\s+\d+(\.\d+)*|Part\s+[IVXLC]+|[A-Z][a-zA-Z0-9\s]{1,50}\n[-=]{2,})$"
    c_pos = 0
    current_page = 0
    id = 0
    e_pos = get_fin(pages)
    while (c_pos < e_pos):
        section= find_next_header(pages , current_page , c_pos , header_pattern , id)
        if section is None:
            break
        sections.append(section)
        id = id+1
    return sections


def find_next_header(pages : list, current_page : int, c_pos : int, header_pattern : str , id : int) -> dict:
    """Search for the next header"""
    
    try:
        pattern = re.compile(header_pattern, re.MULTILINE) #makes it match at the start of each line
    except re.error as e:
        print(f"Invalid regex pattern: {e}")
        return None

    # Loop through the pages starting from the current one
    for i in range(current_page, len(pages)):
        page_text = pages[i]
        
        # Determine where to start searching on this page
        start_search_index = 0 # by default, start at the beginning of the page
        if i == current_page:
            start_search_index = c_pos # if we are on the current page , we start from c_pos
        
        text_to_search = page_text[start_search_index:]
        
        match = pattern.search(text_to_search) #search for the pattern
        
        if match:

            header_start_pos = match.start() + start_search_index
            header_end_pos = match.end() + start_search_index
            
            section = {
                "id" : id,
                "header": match.group().strip(),
                "page": i,
                "start_pos": header_start_pos,
                "end_pos": header_end_pos,
                "text" : text_to_search[:header_start_pos]
            }
            return section
            
    return None

def get_section_text(sections : dict , full_text : str) -> str:
    
    for i, sec in enumerate(sections):
        start = sec["start_pos"]
        end = sections[i+1]["start_pos"] if i+1 < len(sections) else len(full_text)
        sec["text"] = full_text[start:end]

    return sections