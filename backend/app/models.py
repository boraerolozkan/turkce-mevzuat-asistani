from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re


class ChatRequest(BaseModel):
    """Kullanıcıdan gelen soru formatı."""
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Kullanıcının sorusu (3-1000 karakter)"
    )

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        # Boşlukları temizle
        v = v.strip()

        # Minimum uzunluk kontrolü (boşluk temizlendikten sonra)
        if len(v) < 3:
            raise ValueError('Soru en az 3 karakter olmalıdır')

        # Tehlikeli karakterleri filtrele (basit sanitization)
        # Script injection'a karşı
        v = re.sub(r'<[^>]*>', '', v)  # HTML tag'lerini kaldır

        return v


class SourceDoc(BaseModel):
    """Kaynak (Source) bilgisi formatı."""
    source: str
    page_content: str
    score: Optional[float] = None


class ChatResponse(BaseModel):
    """API'nin döneceği cevap formatı."""
    answer: str
    sources: List[SourceDoc]


class ErrorResponse(BaseModel):
    """Hata durumunda dönen format."""
    error: str
    detail: Optional[str] = None
