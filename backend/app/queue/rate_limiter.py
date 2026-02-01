"""
Rate limiting middleware for FastAPI.
Prevents API abuse and ensures fair usage.
"""

from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Rate limit ayarları
RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")  # Dakikada 10 istek
RATE_LIMIT_STORAGE = os.getenv("RATE_LIMIT_STORAGE", "memory://")

# Limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RATE_LIMIT],
    storage_uri=RATE_LIMIT_STORAGE,  # Production'da redis:// kullan
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Rate limit aşıldığında dönen hata."""
    return HTTPException(
        status_code=429,
        detail={
            "error": "rate_limit_exceeded",
            "message": "Çok fazla istek gönderdiniz. Lütfen bir dakika bekleyin.",
            "retry_after": 60
        }
    )


# Decorator olarak kullanım için
def limit(limit_string: str = RATE_LIMIT):
    """
    Rate limit decorator.

    Kullanım:
        @router.post("/chat")
        @limit("5/minute")
        async def chat_endpoint(...):
            ...
    """
    return limiter.limit(limit_string)
