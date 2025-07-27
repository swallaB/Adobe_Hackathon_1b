import fitz  # PyMuPDF
import os

def extract_text_from_collection(collection_name):
    folder_path = os.path.join("data", collection_name, "PDFs")
    pdf_texts = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            pdf_texts[filename] = text
    
    return pdf_texts

if __name__ == "__main__":
    collection_name = "Collection 1"
    pdf_contents = extract_text_from_collection(collection_name)

    for filename, content in pdf_contents.items():
        print(f"\n=== {filename} ===\n")
        print(content[:1000])  # Print first 1000 characters for preview
