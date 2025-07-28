import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the same embedding model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_vector_store():
    index = faiss.read_index("vectorstore/faiss_index")
    with open("vectorstore/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def embed_query(query: str):
    return model.encode([query])[0]

def search_similar_chunks(query: str, top_k=5):
    query_embedding = embed_query(query)
    index, metadata = load_vector_store()

    D, I = index.search(np.array([query_embedding]), top_k)

    results = []
    for i in I[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results
