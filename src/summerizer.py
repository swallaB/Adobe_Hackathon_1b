from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_top_chunks(chunks, max_length=20, min_length=10):
    summaries = []
    for idx, chunk in enumerate(chunks):
        content = chunk["content"].strip()
        # HuggingFace summarizer requires input < 1024 tokens
        if len(content) > 1000:
            content = content[:1000]

        summary = summarizer(content, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]
        summaries.append({
            "chunk_index": idx,
            "summary": summary,
            "source_text": content  # optional: for tracing/debugging
        })
    return summaries

