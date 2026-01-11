import re

def normalize_book_name(name):
    return re.sub(r"[^a-z]", "", name.lower())
