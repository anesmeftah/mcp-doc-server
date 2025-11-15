from os import walk
import typing



def read_files(my_path : str) -> list:
    f = []
    for (root , dirs , files) in walk(my_path):
        f.extend(files)

    return 

