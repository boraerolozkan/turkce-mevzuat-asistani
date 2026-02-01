import os
import glob
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.config import PDF_DIRECTORY


def load_single_pdf(pdf_path: str) -> List[Document]:
    """
    Tek bir PDF dosyasını yükler ve sayfalara böler.

    Args:
        pdf_path: PDF dosyasının tam yolu

    Returns:
        Document listesi (her sayfa bir Document)
    """
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Her sayfaya kaynak bilgisi ekle
        for page in pages:
            page.metadata["source"] = os.path.basename(pdf_path)

        return pages

    except Exception as e:
        print(f"❌ HATA: {pdf_path} okunamadı. Sebep: {e}")
        return []


def load_all_pdfs(directory: str = None, limit: int = None) -> List[Document]:
    """
    Belirtilen klasördeki tüm PDF'leri yükler.

    Args:
        directory: PDF klasörü (varsayılan: PDF_DIRECTORY)
        limit: Test için sadece ilk N PDF'i yükle

    Returns:
        Tüm sayfaların Document listesi
    """
    if directory is None:
        directory = PDF_DIRECTORY

    print(f"📂 {directory} klasöründeki PDF'ler taranıyor...")

    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))

    if not pdf_files:
        print(f"❌ HATA: {directory} konumunda hiç PDF bulunamadı!")
        return []

    print(f"📚 {len(pdf_files)} PDF dosyası bulundu")

    if limit:
        pdf_files = pdf_files[:limit]
        print(f"⚠️ TEST MODU: Sadece ilk {limit} PDF işlenecek")

    all_pages = []

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] İşleniyor: {os.path.basename(pdf_path)}")
        pages = load_single_pdf(pdf_path)
        all_pages.extend(pages)

    print(f"✅ Toplam {len(all_pages)} sayfa yüklendi")
    return all_pages
