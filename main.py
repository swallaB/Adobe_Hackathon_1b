# # src/main.py

# from src.extract_text import extract_text_from_collection
# from src.chunk_text import chunk_by_sections  # assuming you'll implement this here
# import os

# def main():
#     base_path = os.path.join("data")
#     collections = [folder for folder in os.listdir(base_path) if folder.startswith("Collection")]

#     for collection_name in collections:
#         print(f"\nProcessing: {collection_name}")
        
#         # Step 1: Extract PDF text
#         pdf_contents = extract_text_from_collection(collection_name)
        
#         for filename, content in pdf_contents.items():
#             print(f"\n--- {filename} ---")
#             print("Original Text Sample:")
#             print(content[:300])  # preview first 300 chars

#             # Step 2: Semantic Chunking
#             print("\nSemantic Chunks:")
#             chunks = chunk_by_sections(content)
#             for i, chunk in enumerate(chunks):
#                 print(f"\n[Chunk {i+1}]:\n{chunk}\n{'-'*40}")
# 1
# if __name__ == "__main__":
#     main()


# main.py

from src.extract_text import extract_text_from_collection
from src.chunk_text import semantic_chunk_text,augment_chunks_with_sentences
from src.embed_chunks import embed_chunks
from src.query_engine import load_embeddings, search
import os
import json

def main():
    base_path = os.path.join("data")
    output_folder = "output_chunks"
    os.makedirs(output_folder, exist_ok=True)

    collections = "Collection 3"

    
    print(f"\nProcessing: {collections}")
        
        # Step 1: Extract PDF text
    pdf_contents = extract_text_from_collection(collections)

    for filename, content in pdf_contents.items():
        print(f"\n--- {filename} ---")
        print("Original Text Sample:")
        print(content[:300])  # preview first 300 chars

            # Step 2: Semantic Chunking
        print("\nSection-wise Chunks:")
        chunks = semantic_chunk_text(content, filename, collections)
        final_chunks = augment_chunks_with_sentences(chunks)
        for i, chunk in enumerate(final_chunks):
            #print(f"\n[Chunk {i+1} | Section: {chunk['section_title']}]:\n{chunk['text'][:300]}...\n{'-'*40}")

            # # Save chunks to JSON file
            output_path = os.path.join(output_folder, f"{filename.replace('.pdf', '')}_chunks.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(final_chunks, f, ensure_ascii=False, indent=2)

            # # Step 3: Embed the Chunks
        #print(f"Embedding {len(final_chunks)} chunks for: {filename}")
        embed_chunks()  # <-- NEW call

    

# Load all the embedded chunks once at the start
    all_chunks = load_embeddings("output_embeddings")

# Example usage — you can replace this with any query input method
    user_query = "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items"
    results = search(user_query, all_chunks, top_k=5)

# Display results (modify this to fit your format)
    print("\n🔍 Results for your query:\n")
    for i, res in enumerate(results, 1):
        print(f"--- Result #{i} (Score: {res['cross_score']}) ---")
        print(f"📘 Document: {res['document_title']}")
        print(f"📑 Section: {res['section_title']}")
        print(f"📚 Collection: {res['collection']}")
        print(f"📝 Text: {res['text']}\n")

if __name__ == "__main__":
    main()
