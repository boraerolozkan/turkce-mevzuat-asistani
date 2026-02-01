"""
Celery tasks for asynchronous RAG processing.
Handles high-load scenarios by queuing requests.
"""

from celery import Celery
import os

# Redis bağlantı URL'i
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery uygulaması
celery_app = Celery(
    "mevzuat_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery ayarları
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Istanbul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=120,  # 2 dakika max
    worker_prefetch_multiplier=1,  # Her worker tek task alsın
    worker_concurrency=2,  # Aynı anda 2 task (RAM'e göre ayarla)
)


@celery_app.task(bind=True, max_retries=3)
def process_chat_request(self, question: str) -> dict:
    """
    RAG pipeline'ını asenkron olarak çalıştırır.

    Args:
        question: Kullanıcı sorusu

    Returns:
        {"answer": str, "sources": list}
    """
    try:
        # Lazy import - worker başlatıldığında yüklensin
        from app.rag import get_rag_chain

        chain = get_rag_chain()
        result = chain.invoke(question)

        # Sonucu formatla
        sources = []
        for doc in result.get("context", []):
            sources.append({
                "source": doc.metadata.get("source", "Bilinmiyor"),
                "page_content": doc.page_content[:500],  # İlk 500 karakter
            })

        return {
            "answer": result.get("answer", ""),
            "sources": sources
        }

    except Exception as e:
        # Hata durumunda yeniden dene
        self.retry(exc=e, countdown=5)


@celery_app.task
def health_check() -> dict:
    """Worker sağlık kontrolü."""
    return {"status": "healthy", "worker": "celery"}
