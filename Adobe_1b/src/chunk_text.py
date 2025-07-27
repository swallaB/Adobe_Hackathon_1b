# import re

# def semantic_chunk_text(document_text, document_title, collection_name):
#     # Regex to find potential section titles (lines in Title Case)
#     section_pattern = r'(?:\n|^)([A-Z][a-zA-Z0-9\s\-&]+)(?:\n|$)'
#     lines = document_text.splitlines()

#     chunks = []
#     current_section_title = "Introduction"
#     current_section_text = ""

#     for i, line in enumerate(lines):
#         stripped = line.strip()

#         # If this line looks like a section title (Title Case and not too long)
#         if re.fullmatch(r'[A-Z][a-zA-Z0-9\s\-&,]{3,50}', stripped):
#             # Save previous section before switching
#             if current_section_text.strip():
#                 chunks.append({
#                     "text": current_section_text.strip(),
#                     "section_title": current_section_title.strip(),
#                     "document_title": document_title,
#                     "collection": collection_name
#                 })
#             current_section_title = stripped
#             current_section_text = ""
#         else:
#             current_section_text += line + "\n"

#     # Append last chunk
#     if current_section_text.strip():
#         chunks.append({
#             "text": current_section_text.strip(),
#             "section_title": current_section_title.strip(),
#             "document_title": document_title,
#             "collection": collection_name
#         })

#     return chunks

import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')  # Only needs to be run once

def semantic_chunk_text(document_text, document_title, collection_name):
    # Split on title-case headers (section-wise chunking)
    lines = document_text.splitlines()
    chunks = []
    current_section_title = "Introduction"
    current_section_text = ""

    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r'[A-Z][a-zA-Z0-9\s\-&,]{3,50}', stripped):
            if current_section_text.strip():
                # Semantic chunking on current section
                section_chunks = break_into_semantic_chunks(current_section_text.strip(), current_section_title, document_title, collection_name)
                chunks.extend(section_chunks)
            current_section_title = stripped
            current_section_text = ""
        else:
            current_section_text += line + "\n"

    # Final section
    if current_section_text.strip():
        section_chunks = break_into_semantic_chunks(current_section_text.strip(), current_section_title, document_title, collection_name)
        chunks.extend(section_chunks)

    return chunks

def break_into_semantic_chunks(text, section_title, doc_title, collection):
    """Break a section into small sentence-level chunks (3-4 sentences each)."""
    sentences = sent_tokenize(text)
    grouped_chunks = []
    group = []

    for i, sentence in enumerate(sentences):
        group.append(sentence)
        if len(group) >= 3 or i == len(sentences) - 1:
            chunk_text = " ".join(group).strip()
            grouped_chunks.append({
                "text": chunk_text,
                "section_title": section_title.strip(),
                "document_title": doc_title,
                "collection": collection
            })
            group = []

    return grouped_chunks

def augment_chunks_with_sentences(section_chunks, min_words=8):
    new_chunks = []
    for chunk in section_chunks:
        sentences = sent_tokenize(chunk["text"])
        for sent in sentences:
            if len(sent.split()) >= min_words:
                new_chunks.append({
                    "text": sent.strip(),
                    "section_title": chunk["section_title"],
                    "document_title": chunk["document_title"],
                    "collection": chunk["collection"]
                })
    return new_chunks
