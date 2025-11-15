import markdown



def read_md(file_path : str) -> dict:
    with open(file_path , 'r') as f:
        md_text = f.read()

    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(md_text)

    text = {
        "metadata" : md.Meta,
        "text" : md_text
    }

    return text