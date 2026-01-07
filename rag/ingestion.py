from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from pathlib import Path
import yaml



with open("config.yaml") as f:
    config = yaml.safe_load(f)


source_dir = Path("rag/data/sources")
docs = []



for path in source_dir.rglob("*"):
    if path.suffix == ".md" or path.suffix == ".txt":
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    elif path.suffix == ".pdf":
        docs.extend(PyPDFLoader(str(path)).load())
    elif path.suffix == ".docx":
        docs.extend(PyPDFLoader(str(path)).load())
    elif path.suffix == ".html":
        docs.extend(PyPDFLoader(str(path)).load())

if not docs:
    raise ValueError("No documents loaded")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=config["chunk_size"], # Split documents into chunks of size chunk_size
    chunk_overlap=config["chunk_overlap"], # Overlap between chunks
    length_function=len,
    separator=["\n\n", "\n", " ", ""],
    is_separator_regex=False,
    keep_separator=True
)
chunks = splitter.split_documents(docs)


if not chunks: # Check if chunks were generated
    raise ValueError("No chunks generated")

embeddings = OllamaEmbeddings(model=config["embedding_model"]) # Initialize embeddings

# Vector DB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=config["vector_db_path"],
)

vectorstore.persist()

print(f"RAG knowledge base built successfully ({len(chunks)} chunks)")
