# from langchain.text_splitter import MarkdownHeaderTextSplitter
# from typing import List, Dict
# import os, json

# def split_documents_semantic(documents: List[Dict]) -> List[Dict]:
#     """
#     Splits the documents into section-wise chunks with semantic structure.

#     Parameters:
#     - documents: A list of dictionaries, each with:
#         - "text": Full text content of the document
#         - "title": Document title
#         - "page_number": Page number of that chunk

#     Returns:
#     - List of dictionaries with keys:
#         - "doc_title", "section_title", "page_number", "content"
#     """

#     splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "section_title"), ("##", "subsection_title")])
#     final_chunks = []

#     for doc in documents:
#         text = doc["text"]
#         doc_title = doc.get("title", "Unknown Document")
#         page_number = doc.get("page_number", -1)

#         # Split using Markdown headers
#         split_docs = splitter.split_text(text)

#         for split_doc in split_docs:
#             chunk_text = split_doc.page_content.strip()
#             metadata = split_doc.metadata
#             section_title = metadata.get("section_title", "Unknown Section")

#             final_chunks.append({
#                 "doc_title": doc_title,
#                 "section_title": section_title,
#                 "page_number": page_number,
#                 "content": chunk_text
#             })

#     print(f"✅ Split {len(documents)} documents into {len(final_chunks)} structured chunks.")
#     return final_chunks

# def save_chunks_to_json(chunks, output_path="output/chunks.json"):
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(chunks, f, ensure_ascii=False, indent=2)
    
#     print(f"✅ Saved {len(chunks)} chunks to {output_path}")


# chunking.py

# import re
# from typing import List, Dict
# import os, json

# CHUNK_SIZE = 400
# CHUNK_OVERLAP = 50

# def detect_section_title(text: str) -> str:
#     lines = text.strip().splitlines()
#     for line in lines:
#         cleaned = line.strip()

#         if len(cleaned) < 150:
#             if cleaned.isupper():
#                 return cleaned
#             if re.match(r"^\d+(\.\d+)*\s+[A-Z][A-Za-z0-9\s\-:,]*$", cleaned):
#                 return cleaned
#             if any(keyword in cleaned.lower() for keyword in ["introduction", "summary", "overview", "conclusion", "objectives", "background"]):
#                 return cleaned.title()

#     return "Unknown Section"

# def chunk_pages(page_data: List[Dict]) -> List[Dict]:
#     all_chunks = []

#     for entry in page_data:
#         text = entry["text"]
#         doc_title = entry["doc_title"]
#         page_number = entry["page_number"]
#         section_title = detect_section_title(text)

#         words = text.split()
#         start = 0
#         while start < len(words):
#             end = min(start + CHUNK_SIZE, len(words))
#             chunk_text = " ".join(words[start:end])
#             chunk = {
#                 "doc_title": doc_title,
#                 "section_title": section_title,
#                 "page_number": page_number,
#                 "context": chunk_text
#             }
#             all_chunks.append(chunk)
#             start += CHUNK_SIZE - CHUNK_OVERLAP

#     return all_chunks


import re
from nltk.tokenize import sent_tokenize
import nltk
import os,json

nltk.download('punkt')


def break_into_semantic_chunks(text, section_title, doc_title, page_no, max_words=100):
    sentences = sent_tokenize(text)
    grouped_chunks = []
    group = []
    word_count = 0

    for sentence in sentences:
        words = sentence.split()
        group.append(sentence)
        word_count += len(words)

        if word_count >= max_words:
            chunk_text = " ".join(group).strip()
            grouped_chunks.append({
                "text": chunk_text,
                "section_title": section_title.strip(),
                "document_title": doc_title,
                "page_number": page_no
            })
            group = []
            word_count = 0

    if group:
        chunk_text = " ".join(group).strip()
        grouped_chunks.append({
            "text": chunk_text,
            "section_title": section_title.strip(),
            "doc_title": doc_title,
            "page_number": page_no
        })

    return grouped_chunks


def semantic_chunk_text(documents):
    """
    Accepts a list of page-level dicts:
    [{ "title": ..., "text": ..., "page_number": ... }, ...]
    and returns all semantic chunks.
    """
    chunks = []

    for doc in documents:
        document_text = doc["text"]
        document_title = doc["title"]
        page_no = doc["page_number"]

        lines = document_text.splitlines()
        current_section_title = "Introduction"
        current_section_text = ""

        for line in lines:
            stripped = line.strip()
            if re.fullmatch(r'[A-Z][a-zA-Z0-9\s\-&,]{3,50}', stripped):
                if current_section_text.strip():
                    section_chunks = break_into_semantic_chunks(
                        current_section_text.strip(),
                        current_section_title,
                        document_title,
                        page_no
                    )
                    chunks.extend(section_chunks)
                current_section_title = stripped
                current_section_text = ""
            else:
                current_section_text += line + "\n"

        # Final section
        if current_section_text.strip():
            section_chunks = break_into_semantic_chunks(
                current_section_text.strip(),
                current_section_title,
                document_title,
                page_no
            )
            chunks.extend(section_chunks)

    return chunks



def save_chunks_to_json(chunks, output_path="output/chunks.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(chunks)} chunks to {output_path}")
