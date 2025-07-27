# import os
# import json
# import numpy as np
# from sentence_transformers import SentenceTransformer,CrossEncoder
# from sklearn.metrics.pairwise import cosine_similarity

# # Load model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Load all embedded chunks
# def load_embeddings(embedding_dir="output_embeddings"):
#     all_chunks = []
#     for filename in os.listdir(embedding_dir):
#         if not filename.endswith("_embedded.json"):
#             continue

#         filepath = os.path.join(embedding_dir, filename)
#         with open(filepath, 'r', encoding='utf-8') as f:
#             chunks = json.load(f)
#             all_chunks.extend(chunks)

#     return all_chunks

# # Search the top-k matching chunks
# def search(query, all_chunks, top_k=5):
#     query_embedding = model.encode([query])[0]
#     chunk_embeddings = np.array([chunk["embedding"] for chunk in all_chunks])

#     similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
#     top_indices = similarities.argsort()[::-1][:top_k]

#     results = []
#     for idx in top_indices:
#         chunk = all_chunks[idx]
#         results.append({
#             "similarity": round(similarities[idx], 3),
#             "text": chunk["text"],
#             "section_title": chunk["section_title"],
#             "document_title": chunk["document_title"],
#             "collection": chunk["collection"]
#         })

#     return results

from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import json

# Load both models
bi_encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Fast for initial retrieval
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # For re-ranking

def load_embeddings(embedding_dir="output_embeddings"):
    all_chunks = []
    for filename in os.listdir(embedding_dir):
        if not filename.endswith("_embedded.json"):
            continue

        filepath = os.path.join(embedding_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)

    return all_chunks

def search(query, all_chunks, top_k=5, initial_k=20):
    # Step 1: Initial retrieval using Bi-encoder
    query_embedding = bi_encoder.encode([query])[0]
    chunk_embeddings = np.array([chunk["embedding"] for chunk in all_chunks])
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:initial_k]

    # Step 2: Create candidate pairs for cross-encoder
    candidate_chunks = [all_chunks[i] for i in top_indices]
    cross_input_pairs = [[query, chunk["text"]] for chunk in candidate_chunks]

    # Step 3: Re-rank with cross-encoder
    cross_scores = cross_encoder.predict(cross_input_pairs)
    reranked = sorted(zip(cross_scores, candidate_chunks), key=lambda x: x[0], reverse=True)

    # Step 4: Return top-k re-ranked results
    final_results = []
    for score, chunk in reranked[:top_k]:
        final_results.append({
            "cross_score": round(float(score), 3),
            "text": chunk["text"],
            "section_title": chunk["section_title"],
            "document_title": chunk["document_title"],
            "collection": chunk["collection"]
        })

    return final_results

