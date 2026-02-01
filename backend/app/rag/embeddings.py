from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL

# Singleton pattern - embedding modeli bir kez yüklensin
_embeddings_instance = None


def get_embeddings():
    """
    HuggingFace embedding modelini döndürür.
    Türkçe için optimize edilmiş multilingual model kullanır.
    """
    global _embeddings_instance

    if _embeddings_instance is None:
        print(f"🧠 Embedding modeli yükleniyor: {EMBEDDING_MODEL}")
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("✅ Embedding modeli hazır")

    return _embeddings_instance
