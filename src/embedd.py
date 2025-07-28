import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

def embed_chunks(chunks, model_name="all-MiniLM-L6-v2"):
    """
    Embeds chunks and stores them in FAISS with corresponding metadata.
    """
    model = SentenceTransformer(model_name)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save index and metadata separately
    os.makedirs("vectorstore", exist_ok=True)
    faiss.write_index(index, "vectorstore/faiss_index")

    # Save metadata with doc_title, section_title, page_number, content
    clean_metadata = []
    for chunk in chunks:
        clean_metadata.append({
            "doc_title": chunk.get("doc_title", "Unknown"),
            "section_title": chunk.get("section_title", "Unknown"),
            "page_number": chunk.get("page_number", -1),
            "content": chunk["text"]
        })

    with open("vectorstore/metadata.pkl", "wb") as f:
        pickle.dump(clean_metadata, f)

    print(f"✅ Embedded and stored {len(clean_metadata)} chunks with detailed metadata.")


def load_faiss_index():
    index = faiss.read_index("vectorstore/faiss_index")
    with open("vectorstore/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata
