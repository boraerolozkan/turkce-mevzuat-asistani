from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config import QDRANT_URL, COLLECTION_NAME, RETRIEVER_K
from app.rag.embeddings import get_embeddings


def get_retriever():
    """
    Qdrant vector store üzerinde semantic search yapan retriever döndürür.
    """
    embeddings = get_embeddings()
    client = QdrantClient(url=QDRANT_URL)

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K}
    )

    return retriever


def search_documents(query: str, k: int = None):
    """
    Verilen sorguya en yakın dokümanları getirir.

    Args:
        query: Arama sorgusu
        k: Kaç sonuç getirileceği (varsayılan: RETRIEVER_K)

    Returns:
        İlgili doküman listesi
    """
    if k is None:
        k = RETRIEVER_K

    embeddings = get_embeddings()
    client = QdrantClient(url=QDRANT_URL)

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    results = vectorstore.similarity_search_with_score(query, k=k)
    return results
