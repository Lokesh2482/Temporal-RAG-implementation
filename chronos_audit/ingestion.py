import os
import pandas as pd

def load_local_books(root_dir="."):
    """
    Loads local_*.txt files using pure Python.
    Windows-safe. No Pathway dependency.
    """
    books = []

    for fname in os.listdir(root_dir):
        if fname.startswith("local_") and fname.endswith(".txt"):
            book_name = fname.replace("local_", "").replace(".txt", "")
            with open(os.path.join(root_dir, fname), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            books.append({
                "book_name": book_name,
                "content": content
            })

    if not books:
        raise RuntimeError("No local_*.txt files found in project root.")

    return pd.DataFrame(books)
