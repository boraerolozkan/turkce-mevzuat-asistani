from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Metin parçalayıcı oluşturur.

    Türkçe metinler için optimize edilmiş ayarlar:
    - chunk_size: 800 karakter (optimal anlam korunması için)
    - chunk_overlap: 100 karakter (cümle bölünmelerini önlemek için)
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",  # Paragraf sonu
            "\n",    # Satır sonu
            ".",     # Cümle sonu
            ";",     # Noktalı virgül
            ",",     # Virgül
            " ",     # Boşluk
            ""       # Karakter
        ]
    )


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Doküman listesini daha küçük parçalara böler.

    Args:
        documents: Bölünecek doküman listesi

    Returns:
        Parçalanmış doküman listesi
    """
    if not documents:
        return []

    text_splitter = get_text_splitter()

    print(f"✂️ {len(documents)} doküman parçalanıyor...")
    print(f"   Chunk boyutu: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP}")

    chunks = text_splitter.split_documents(documents)

    print(f"✅ {len(chunks)} parça oluşturuldu")
    print(f"   Ortalama: {len(chunks) / len(documents):.1f} parça/doküman")

    return chunks


def chunk_text(text: str, metadata: dict = None) -> List[Document]:
    """
    Tek bir metni parçalara böler.

    Args:
        text: Bölünecek metin
        metadata: Eklenecek metadata

    Returns:
        Document listesi
    """
    if metadata is None:
        metadata = {}

    text_splitter = get_text_splitter()
    chunks = text_splitter.create_documents(
        texts=[text],
        metadatas=[metadata]
    )

    return chunks
