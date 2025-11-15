from os import walk
import typing
from os import stat

#reading files in a specific dir
def read_files(my_path : str) -> list:
    f = []
    for (root , dirs , files) in walk(my_path):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".md") or file.endswith(".csv"):
                meta = get_file_metadata(my_path + "/" + file)
                file_dict = {
                    "file_name" : file , 
                    "metadata" : meta ,
                    "file_path" : my_path + file
                }
                f.append(file_dict)

    return f


def get_file_metadata(file_path : str):
    stats = stat(file_path)
    result = {
        "size" :stats.st_size ,
        "last_modified" : stats.st_mtime
    }
    return result

