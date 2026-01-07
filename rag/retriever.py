from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

embeddings = OllamaEmbeddings(model=config["embedding_model"]
                            )

def get_retriever():
    vectorstore= Chroma(
        collection_name="vulnerability_knowledge",
        persist_directory=config["vector_db_path"],
        embedding_function = embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": config["top_k_retrieval"]})