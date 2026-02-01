from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import chat
from app.queue.rate_limiter import limiter

app = FastAPI(
    title="Türkçe Mevzuat Asistanı API",
    description="RAG tabanlı hukuk asistanı backend",
    version="1.0.0"
)

# Rate Limiter'ı ekle
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler belirle
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(chat.router, prefix="/api")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mevzuat Asistanı API Çalışıyor"}


@app.get("/health")
def health_check():
    """Detaylı sağlık kontrolü."""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "rate_limiter": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
