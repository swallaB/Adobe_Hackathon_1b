# 📘 Document Summarization Engine

## Overview

In many industries, professionals need to extract relevant information from lengthy PDFs like brochures, manuals, contracts, and reports. Manually reviewing such documents is time-consuming and inefficient. Our solution presents a general-purpose document ingestion and summarization engine that allows users to query these documents in natural language and receive relevant summaries with source traceability.

This tool is designed to work across multiple domains including travel planning, procurement, event coordination, and more. It offers semantic understanding, high-speed retrieval, text summarization.

---

## 🧠 Approach

The pipeline is composed of five modular stages:

### 1. PDF Parsing
We use **PyMuPDF (fitz)** to extract text and metadata (like page numbers) from uploaded PDF files. This preserves the structure and traceability of content.

### 2. Semantic Chunking
Using **NLTK**, raw text is tokenized into sentences and grouped into coherent semantic chunks and used regex based classification for sections. This step ensures chunks are contextually rich and summarization-ready.

### 3. Embedding & Indexing
Each chunk is encoded using **SentenceTransformers** (`all-MiniLM-L6-v2`) into dense vectors. These are indexed using **FAISS**, enabling fast and scalable similarity search.

### 4. Semantic Retrieval
When a user submits a query, it is embedded into the same vector space. We retrieve the top-k most relevant chunks using FAISS. This ensures accurate retrieval based on meaning, not just keywords.

### 5. Summarization
Top-ranked results are summarized using HuggingFace’s transformer model `distilbart-cnn-12-6`. Summaries are concise, informative, and provide clear answers aligned with the user query.

---

## 🔎 Output Format

Each result contains:
- Source document and page number
- Original matched text
- Summarized output
- Relevance ranking

Results are returned in JSON format for easy integration with other systems or UI components.

---

## 🔧 Tech Stack

- **Python 3.10**
- **PyMuPDF (fitz)** – PDF parsing
- **NLTK** – Sentence tokenization
- **FAISS** – Vector indexing and search
- **SentenceTransformers** – Embedding
- **Transformers (HuggingFace)** – Summarization

---

## 🚀 Features

- Domain-agnostic PDF question answering
- Fast semantic search with vector similarity
- Transformer-powered abstractive summaries
- Traceability with page references
- Modular, scalable, and Docker-compatible architecture

This engine transforms static PDFs into interactive, queryable knowledge—saving time and improving access to critical insights across diverse use cases.

---

