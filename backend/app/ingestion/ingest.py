"""
Veri yükleme scripti.
PDF dosyalarını okur, parçalar ve Qdrant'a yükler.

Kullanım:
    python -m app.ingestion.ingest
    python -m app.ingestion.ingest --limit 10  # Test için sadece 10 PDF
"""

import argparse
from app.ingestion.pdf_loader import load_all_pdfs
from app.ingestion.chunker import chunk_documents
from app.ingestion.indexer import index_documents, get_collection_info
from app.config import PDF_DIRECTORY


def run_ingestion(pdf_directory: str = None, limit: int = None):
    """
    Tam veri yükleme pipeline'ını çalıştırır.

    Args:
        pdf_directory: PDF dosyalarının bulunduğu klasör
        limit: Test için sadece ilk N PDF'i işle
    """
    if pdf_directory is None:
        pdf_directory = PDF_DIRECTORY

    print("=" * 60)
    print("MEVZUAT VERİ YÜKLEME PIPELINE'I")
    print("=" * 60)

    # 1. PDF'leri yükle
    print("\n📚 ADIM 1: PDF'ler yükleniyor...")
    documents = load_all_pdfs(directory=pdf_directory, limit=limit)

    if not documents:
        print("❌ Yüklenecek doküman bulunamadı!")
        return

    # 2. Parçalara böl
    print("\n✂️ ADIM 2: Dokümanlar parçalanıyor...")
    chunks = chunk_documents(documents)

    # 3. Qdrant'a yükle
    print("\n🚀 ADIM 3: Qdrant'a yükleniyor...")
    count = index_documents(chunks)

    # 4. Sonuç
    print("\n" + "=" * 60)
    print("YÜKLEME TAMAMLANDI")
    print("=" * 60)

    info = get_collection_info()
    print(f"\nKoleksiyon bilgileri:")
    print(f"  - Ad: {info.get('name', 'N/A')}")
    print(f"  - Vektör sayısı: {info.get('vectors_count', 'N/A')}")
    print(f"  - Durum: {info.get('status', 'N/A')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mevzuat PDF'lerini Qdrant'a yükle")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Test için sadece ilk N PDF'i işle"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default=None,
        help="PDF klasörü (varsayılan: config'den)"
    )

    args = parser.parse_args()
    run_ingestion(pdf_directory=args.directory, limit=args.limit)
