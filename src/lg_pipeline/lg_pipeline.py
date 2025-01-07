import os
import re
import multiprocessing
import unicodedata

# Disable Hugging Face symlink warnings on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from transformers import pipeline, logging, AutoTokenizer
logging.set_verbosity_error()

# We'll load the tokenizer for DistilBart to chunk by tokens
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

def clean_text(text: str) -> str:
    """
    Removes or normalizes unusual Unicode characters that can break tokenization.
    """
    # Example: strip combining chars, limit to BMP plane, etc.
    return "".join(ch for ch in unicodedata.normalize("NFKD", text) if ord(ch) < 65536)

def chunk_text_by_tokens(text: str, max_tokens=800):
    """
    Splits text into chunks of up to 'max_tokens' tokens (approx).
    We use the DistilBart tokenizer to ensure we do not exceed model limits.
    """
    # Clean the text
    cleaned = clean_text(text)
    # Encode the entire text into token IDs
    input_ids = tokenizer.encode(cleaned, truncation=False, add_special_tokens=False)
    
    # We'll slice the input_ids in chunks of 'max_tokens'
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i : i + max_tokens]
        # Decode back to text so we can feed it to the summarization pipeline
        yield tokenizer.decode(chunk_ids, skip_special_tokens=True)

class Node:
    # Represents a single step in the pipeline
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def run(self, input_data):
        return self.func(input_data)

class Graph:
    # Orchestrates multiple nodes in sequence
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self, initial_input):
        data = initial_input
        for node in self.nodes:
            data = node.run(data)
        return data

def extract_metadata_func(text: str):
    """
    Uses QA pipeline to extract basic metadata (title, authors, publication date).
    """
    qa_pipe = pipeline(
        "question-answering", 
        model="distilbert-base-uncased-distilled-squad",
        device=-1
    )

    text_clean = clean_text(text)
    
    # Basic QA for title, authors, date
    title_ans = qa_pipe({"question": "What is the title of the paper?", "context": text_clean})
    authors_ans = qa_pipe({"question": "Who are the authors?", "context": text_clean})
    date_ans = qa_pipe({"question": "When was the paper published?", "context": text_clean})

    return {
        "title": title_ans.get("answer", "Unknown Title"),
        "authors": authors_ans.get("answer", "Unknown Authors"),
        "publication_date": date_ans.get("answer", "Unknown Date"),
        "full_text": text_clean
    }

def extract_findings_and_methodology_func(data: dict):
    """
    Summarizes the text in token-based chunks, focusing on methodology and key findings.
    """
    summ_pipe = pipeline(
        "summarization", 
        model="sshleifer/distilbart-cnn-12-6", 
        device=-1, 
        truncation=True
    )
    text_chunks = list(chunk_text_by_tokens(data["full_text"], max_tokens=800))
    partial_summaries = []
    for ch in text_chunks:
        prompt_text = "Focus on methodology and key findings:\n" + ch
        summary = summ_pipe(prompt_text, max_length=60, min_length=20, do_sample=False, truncation=True)
        partial_summaries.append(summary[0]["summary_text"] if summary else "")

    data["methodology_findings"] = " ".join(partial_summaries)
    return data

def generate_summary_and_keywords_func(data: dict):
    """
    Creates a global summary in token-based chunks, 
    and extracts keywords by naive frequency.
    """
    summ_pipe = pipeline(
        "summarization", 
        model="sshleifer/distilbart-cnn-12-6", 
        device=-1, 
        truncation=True
    )

    text_chunks = list(chunk_text_by_tokens(data["full_text"], max_tokens=800))
    all_summaries = []
    for ch in text_chunks:
        partial_sum = summ_pipe(ch, max_length=60, min_length=20, do_sample=False, truncation=True)
        all_summaries.append(partial_sum[0]["summary_text"] if partial_sum else "")

    data["global_summary"] = " ".join(all_summaries)

    # Simple frequency-based keyword extraction
    words = re.findall(r"\w+", data["full_text"].lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    stopwords = {"the","of","and","in","to","a","is","that","it","for","was","with","are","this","which"}
    keywords = [w for w, c in sorted(freq.items(), key=lambda x: x[1], reverse=True)
                if w not in stopwords and len(w) > 3][:10]
    data["keywords"] = keywords
    return data

def run_pipeline_on_pdf(pdf_path: str, extract_text_func) -> dict:
    """
    Reads the PDF via extract_text_func, executes the pipeline, returns final dict.
    """
    multiprocessing.freeze_support()

    # 1) Extract text
    raw_text = extract_text_func(pdf_path)

    # 2) Create nodes
    metadata_node = Node("metadata_node", extract_metadata_func)
    findings_node = Node("findings_node", extract_findings_and_methodology_func)
    summary_keywords_node = Node("summary_keywords_node", generate_summary_and_keywords_func)

    # 3) Create graph
    pipeline_graph = Graph([metadata_node, findings_node, summary_keywords_node])

    # 4) Execute pipeline
    result = pipeline_graph.execute(raw_text)

    # 5) Build final dict
    final_data = {
        "title": result["title"],
        "authors": result["authors"],
        "publication_date": result["publication_date"],
        "methodology_findings": result.get("methodology_findings", ""),
        "global_summary": result.get("global_summary", ""),
        "keywords": result.get("keywords", [])
    }
    return final_data

if __name__ == "__main__":
    from pdf_utils.extract import extract_text_from_pdf

    # Example path
    pdf_path = r"C:\Users\jnv77\Documents\Astrafy\challenge-two\papers\paper1.pdf"
    final_data = run_pipeline_on_pdf(pdf_path, extract_text_from_pdf)
    print("\nPipeline Output:\n", final_data)
