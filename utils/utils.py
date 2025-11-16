def find_nth(ch : str , sub : str , occ : int) -> int:
    index = -1

    for i in range(1 , occ):
        index = ch.find(sub , index + 1)
        if index == -1:
            return -1

    return index


def get_fin(pages : list) -> int:
    fin = 0
    for page in pages:
        fin = fin + len(page)
    
    return fin