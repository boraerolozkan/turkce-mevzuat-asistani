from fastapi import APIRouter, HTTPException, Request
from app.models import ChatRequest, ChatResponse, SourceDoc
from app.rag import get_rag_chain
from app.queue.rate_limiter import limiter

router = APIRouter()
rag_chain = get_rag_chain()


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")  # Dakikada 10 istek limiti
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Kullanıcı sorusunu alır ve RAG pipeline ile cevap üretir.

    Rate Limit: 10 istek/dakika (IP başına)
    """
    try:
        # RAG zincirini çalıştır
        result = rag_chain.invoke(chat_request.question)

        # Dokümanları API formatına çevir
        source_documents = []
        for doc in result["context"]:
            source_documents.append(
                SourceDoc(
                    source=doc.metadata.get("source", "Bilinmiyor"),
                    page_content=doc.page_content[:500],  # İlk 500 karakter
                    score=0.0
                )
            )

        return ChatResponse(
            answer=result["answer"],
            sources=source_documents
        )

    except Exception as e:
        print(f"Hata detayı: {e}")
        raise HTTPException(status_code=500, detail=str(e))
