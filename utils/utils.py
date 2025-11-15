def find_nth(ch : str , sub : str , occ : int) -> int:
    index = -1

    for i in range(occ):
        index = ch.find(sub , index + 1)
        if index == -1:
            return -1

    return index