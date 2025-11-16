from modules import file_reader , pdf_extractor , chuncker
from modules.file_reader import return_files_names , return_file_path
from modules.pdf_extractor import clean_text


my_files = file_reader.read_files("/home/ameftah/Youtube")
print(return_files_names(my_files))

clean_pdf = clean_text(return_file_path(my_files , 6))