from langchain.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import yaml

with open("config.yaml") as f: # Open config file
    config = yaml.safe_load(f)

loader = DirectoryLoader("rag/data/sources", # Load documents from sources directory
         glob="**/*.{md,txt,pdf}", # Load all markdown, txt, and pdf files
         show_progress=True)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter( 
    chunk_size=config["chunk_size"], # Split documents into chunks of size chunk_size
    chunk_overlap=config["chunk_overlap"], # Overlap between chunks
    length_function=len,
    separator=["\n\n", "\n", " ", ""],
    is_separator_regex=False,
    keep_separator=True
)
chunks = splitter.split_documents(docs) # Split documents into chunks


if not chunks: # Check if chunks were generated
    raise ValueError("No chunks generated")
if not docs: # Check if documents were loaded
    raise ValueError("No documents loaded")

embeddings = OllamaEmbeddings(model=config["embedding_model"]) # Initialize embeddings

Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=config["vector_db_path"],
    
) # Initialize Chroma vector database

print("RAG knowledge base built successfully")