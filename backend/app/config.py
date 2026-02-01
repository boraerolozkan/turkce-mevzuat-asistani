import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant Ayarları
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "mevzuat_db")

# Embedding Model Ayarları
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
EMBEDDING_DIMENSION = 384  # MiniLM modeli için standart boyut

# Ollama/LLM Ayarları
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))

# RAG Ayarları
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))  # Kaç chunk getirilecek

# Chunking Ayarları
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# Veri Yolları
PDF_DIRECTORY = os.getenv("PDF_DIRECTORY", "/data/mevzuat")
