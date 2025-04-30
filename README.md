# 🧠 Generative Document Search System using LlamaIndex & HuggingFace Embeddings

This project is a Generative AI-powered document search engine that enables users to ask natural language queries against a collection of unstructured documents (PDFs, DOCX, CSVs). It leverages **LlamaIndex**, **OpenAI LLMs**, and **HuggingFace Embeddings** to perform semantic search over documents.

---

## 🚀 Project Overview

### 📂 1. Loading and Preprocessing Documents

**Objective:** Load and standardize text from various document formats (CSV, PDF, DOCX) into a unified structure.

- **CSV**: Only the relevant text column (`summary`) is selected.
- **PDF**: Text is extracted page-by-page using `PyMuPDF` (`fitz`).
- **DOCX**: Paragraphs are extracted using `python-docx`.

> ✅ **Outcome:** A list of `Document` objects ready for further processing.

---

### 🧩 2. Chunking Documents using SimpleNodeParser

**Objective:** Large documents are broken into smaller, manageable chunks (nodes) using `SimpleNodeParser`.

- **Why chunking?**
  - Prevents LLM token limit issues.
  - Improves retrieval granularity.
  
> ✅ **Outcome:** A list of semantic text chunks ready for embedding and indexing.

---

### 🤖 3. Initializing the Language Model (LLM)

**Objective:** Initialize an LLM (e.g., OpenAI's GPT-3.5 Turbo) to use for reasoning during query time.

- `OpenAI` is used as the LLM provider via the `llama_index.llms.openai.OpenAI` interface.
- Requires an OpenAI API Key.

> ✅ **Outcome:** An LLM interface configured to answer semantic queries.

---

### 🧠 4. Building the Vector Index

**Objective:** Embed the document nodes into high-dimensional vectors and build a searchable index.

- Uses `HuggingFaceEmbedding` with `all-MiniLM-L6-v2` for local embedding.
- `VectorStoreIndex` is constructed from the embedded nodes.
- Global `Settings` object is used to set LLM and embedding models.

> ✅ **Outcome:** A memory-efficient semantic vector index ready for querying.

---

### 🔍 5. Query Engine

**Objective:** Allow users to input natural language questions and get relevant answers from the indexed documents.

- A `query_engine` is created from the index.
- User questions are transformed into vectors and matched with the most relevant chunks.
- Results are synthesized into a natural language answer using the LLM.

> ✅ **Outcome:** A conversational QA system over your custom documents.

---

## ⚠️ 6. Possible Challenges

| Challenge | Explanation |
|----------|-------------|
| **Large Document Size** | Chunking needs to balance context and relevance. Over-chunking can reduce semantic integrity. |
| **Poor Quality PDFs** | Scanned PDFs or images won't yield good text unless OCR is used. |
| **Embedding Accuracy** | Quality of embeddings depends on model used. `MiniLM` is fast but not always optimal for complex queries. |
| **Latency** | Querying an LLM like GPT-3.5 can introduce noticeable latency for each question. |
| **Memory Usage** | Storing large vector indices in memory may cause issues in resource-constrained environments. |
| **File Format Handling** | Errors during parsing non-standard or corrupted files can break ingestion. |

---

## 🧰 7. Requirements

- Python ≥ 3.8
- `llama-index`
- `openai`
- `sentence-transformers`
- `PyMuPDF` (for PDF parsing)
- `python-docx` (for DOCX parsing)
- `pandas`

---



## 📚 8. Concepts Used
**LlamaIndex** - A lightweight framework designed to help developers connect LLMs to custom, domain-specific data. It allows efficient indexing and retrieval of textual content using semantic search.

**Embeddings** - Used to convert text into dense vectors that represent the semantic meaning of content. This project uses HuggingFace’s `all-MiniLM-L6-v2` model for embedding documents.

**OpenAI GPT** - GPT-3.5-turbo is used for query interpretation and response generation. It interprets user questions and uses indexed document chunks to generate coherent and contextually relevant answers.

**Vector Stores** - Enable similarity-based search by comparing embeddings of user queries with embeddings of document chunks. Relevant results are passed to the LLM for final synthesis.


## 🙌 9. Key Contributions

You are welcome to fork this project and explore enhancements like:
- Adding OCR support for scanned PDFs.
- Integrating Streamlit or Gradio UI.
- Caching embeddings to optimize repeated runs.
- Replacing OpenAI with a local LLM like Mistral or LLaMA.
- Storing and querying the index from disk for persistence.


## 🏁 10. Run Instructions

```bash
pip install llama-index openai sentence-transformers python-docx pandas pymupdf
