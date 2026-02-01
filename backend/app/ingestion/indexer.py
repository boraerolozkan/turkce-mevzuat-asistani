from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import (
    QDRANT_URL,
    COLLECTION_NAME,
    EMBEDDING_DIMENSION
)
from app.rag.embeddings import get_embeddings


def create_collection(client: QdrantClient, collection_name: str = None):
    """
    Qdrant'ta yeni bir koleksiyon oluşturur.

    Args:
        client: Qdrant client
        collection_name: Koleksiyon adı
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME

    # Varsa sil
    try:
        client.delete_collection(collection_name)
        print(f"🗑️ Eski '{collection_name}' koleksiyonu silindi")
    except Exception:
        pass

    # Yeni oluştur
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=models.Distance.COSINE
        )
    )
    print(f"✅ '{collection_name}' koleksiyonu oluşturuldu")


def index_documents(
    documents: List[Document],
    collection_name: str = None,
    recreate: bool = True
) -> int:
    """
    Dokümanları Qdrant'a yükler.

    Args:
        documents: Yüklenecek dokümanlar
        collection_name: Koleksiyon adı
        recreate: Koleksiyonu yeniden oluştur

    Returns:
        Yüklenen doküman sayısı
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME

    if not documents:
        print("❌ Yüklenecek doküman yok!")
        return 0

    embeddings = get_embeddings()
    client = QdrantClient(url=QDRANT_URL)

    if recreate:
        create_collection(client, collection_name)

    print(f"🚀 {len(documents)} doküman Qdrant'a yükleniyor...")

    Qdrant.from_documents(
        documents,
        embeddings,
        url=QDRANT_URL,
        collection_name=collection_name,
        force_recreate=False  # Yukarıda manuel oluşturduk
    )

    print(f"✅ {len(documents)} doküman başarıyla yüklendi!")
    return len(documents)


def get_collection_info(collection_name: str = None) -> dict:
    """
    Koleksiyon hakkında bilgi döndürür.
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME

    client = QdrantClient(url=QDRANT_URL)

    try:
        info = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status
        }
    except Exception as e:
        return {"error": str(e)}
