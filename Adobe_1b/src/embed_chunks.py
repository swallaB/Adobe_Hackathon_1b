from sentence_transformers import SentenceTransformer
import json
import os
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(input_dir="output_chunks", output_dir="output_embeddings"):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.endswith("_chunks.json"):
            continue

        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        texts = [chunk["text"] for chunk in chunks]
        embeddings = model.encode(texts, show_progress_bar=True)

        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i].tolist()

        output_path = os.path.join(output_dir, filename.replace("_chunks.json", "_embedded.json"))
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        print(f"✅ Embedded: {filename} → {output_path}")

if __name__ == "__main__":
    embed_chunks()
