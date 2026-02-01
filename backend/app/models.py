from pydantic import BaseModel
from typing import List, Optional

# Kullanıcıdan gelen soru formatı
class ChatRequest(BaseModel):
    question: str

# Kaynak (Source) bilgisi formatı
class SourceDoc(BaseModel):
    source: str
    page_content: str
    score: Optional[float] = None

# API'nin döneceği cevap formatı
class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDoc]