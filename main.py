from src.loader import load_all_pdfs
from src.splitter import semantic_chunk_text,save_chunks_to_json
from src.embedd import  embed_chunks
from src.query_engine import search_similar_chunks
from src.summerizer import summarize_top_chunks
from datetime import datetime
import json
import os


def main():
    print("🚀 Starting PDF loading pipeline...")
    input_path = "data\Collection 1\challenge1b_input.json"
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona = input_data.get("persona", "")
    job = input_data.get("job_to_be_done", "")
    query = job 
    docs=input_data.get("documents")
    

    
    DOCUMENTS_DIR = "data\Collection 1\PDFs"
    documents = load_all_pdfs(DOCUMENTS_DIR)

    #print(f"✅ Loaded {len(documents)} documents.\n")

    # Step 2: Split documents semantically into chunks
    chunks =semantic_chunk_text(documents)
    print(f"✅ Split into {len(chunks)} semantic chunks.\n")
    save_chunks_to_json(chunks, "output/chunks.json")

    
    embed_chunks(chunks)
    print("🏁 Pipeline completed successfully!\n")

    
    results = search_similar_chunks(query, top_k=5)
    summaries = summarize_top_chunks(results)

    metadata = {
        "input_documents": list({chunk["filename"] for chunk in docs}),  # Unique titles
        "persona": persona,  # Can be parameterized
        "job_to_be_done": job,
        "processing_timestamp": datetime.now().isoformat()
    }

    extracted_sections = []

    for rank, chunk in enumerate(results, start=1):
        extracted_sections.append({
            "document": chunk["doc_title"],
            "section_title": chunk["section_title"],
            "importance_rank": rank,
            "page_number": chunk["page_number"]
        })

    subsection_analysis = []
    for idx, chunk in enumerate(results):
        subsection_analysis.append({
            "document": chunk["doc_title"],
            "refined_text": summaries[idx]["summary"],
            "page_number": chunk["page_number"]
        })
    final_output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4)




if __name__ == "__main__":
    main()