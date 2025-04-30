import warnings
warnings.filterwarnings("ignore")

from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Document
from llama_index.core import Settings
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import TextNode
from llama_index.llms.openai import OpenAI

# from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

import os
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for Word files
import pandas as pd



def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.endswith(".csv"):
            # Read the CSV file with only the necessary columns
            df = pd.read_csv(filepath, usecols=['summary'])  # Adjust columns as needed
            text = df.to_string(index=False)
            documents.append(Document(text=text))

        elif filename.endswith(".pdf"):
            try:
                with fitz.open(filepath) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    if text.strip():  # Ensure it's not empty
                        documents.append(Document(text=text))
            except Exception as e:
                print(f"Error reading PDF file {filename}: {e}")

        elif filename.endswith(".docx"):
            try:
                doc = docx.Document(filepath)
                text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                if text.strip():
                    documents.append(Document(text=text))
            except Exception as e:
                print(f"Error reading DOCX file {filename}: {e}")

    return documents


# Step 2: Chunk documents (node parsing)
def chunk_documents(documents, chunk_size=512):
    parser = SimpleNodeParser.from_defaults(chunk_size=chunk_size)
    nodes = parser.get_nodes_from_documents(documents)
    return nodes


# Step 3: Initialize LLM (free API key or dummy model)
def initialize_llm():
    llm = OpenAI(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" compatible
        api_key="api_key"
    )
    return llm


# Step 4: Build Vector Index



def build_index(nodes, llm):
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Set global settings instead of using ServiceContext
    Settings.llm = llm
    Settings.embed_model = embed_model

    index = VectorStoreIndex(nodes)
    return index



# Step 5: Query system
def query_index(index, query_text):
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return response.response  # Now response is an object; use .response


# Main execution
if __name__ == "__main__":
    # Load documents
    docs = load_documents("./data")
    print(f"Loaded {len(docs)} documents.")

    # Chunk documents
    nodes = chunk_documents(docs)
    print(f"Generated {len(nodes)} chunks.")

    # Initialize LLM
    llm = initialize_llm()

    # Build index
    index = build_index(nodes, llm)
    print("Index built successfully.")

    # Example query
    while True:
        user_query = input("Ask your question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer = query_index(index, user_query)
        print("\nAnswer:", answer)
