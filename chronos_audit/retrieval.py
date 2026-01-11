def retrieve_documents(index, query):
    try:
        bm25_docs = index["bm25"].invoke(query)
        vec_docs = index["vector"].similarity_search(query, k=50)
        return list({d.page_content: d for d in bm25_docs + vec_docs}.values())
    except:
        return []
