import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .config import CONFIG

def build_indices(book_df):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFIG["CHUNK_SIZE"],
        chunk_overlap=CONFIG["CHUNK_OVERLAP"]
    )

    embedder = HuggingFaceEmbeddings(model_name=CONFIG["EMBED_MODEL"])
    indices = {}

    for _, row in book_df.iterrows():
        chunks = splitter.split_text(row["content"])
        docs = [
            Document(page_content=c, metadata={"source": row["book_name"]})
            for c in chunks
        ]

        if not docs:
            continue

        bm25 = BM25Retriever.from_documents(docs)
        bm25.k = 50

        safe_name = re.sub(r"[^a-zA-Z0-9]", "", row["book_name"])[:50]
        vector = Chroma.from_documents(
            docs,
            embedder,
            collection_name=f"chronos_{safe_name}"
        )

        indices[row["book_name"]] = {
            "bm25": bm25,
            "vector": vector
        }

    return indices
