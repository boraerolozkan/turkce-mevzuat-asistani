from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import OLLAMA_BASE_URL, LLM_MODEL, LLM_TEMPERATURE

# Türkçe mevzuat asistanı için özelleştirilmiş prompt
RAG_PROMPT_TEMPLATE = """
Sen yardımcı bir hukuk asistanısın. Verilen bağlamı (context) kullanarak soruyu cevapla.

Kurallar:
1. Sadece verilen metne sadık kal, ancak metindeki anlamı birleştirerek açıklayıcı ol.
2. Eğer metinde tam cevap yoksa, "Verilen belgelerde bu bilgi doğrudan yer almıyor ancak şunlardan bahsediliyor..." diyerek elindeki bilgiyi özetle.
3. Asla tamamen uydurma cevap verme.
4. Mümkünse hangi kanun veya yönetmelikten alıntı yaptığını belirt.

Bağlam:
{context}

Soru:
{question}

Cevap:
"""


def get_llm():
    """
    Ollama LLM instance'ı döndürür.
    """
    print(f"🦙 Ollama'ya bağlanılıyor: {OLLAMA_BASE_URL}")

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        base_url=OLLAMA_BASE_URL
    )

    return llm


def get_prompt():
    """
    RAG için prompt template döndürür.
    """
    return ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


def generate_response(context: str, question: str) -> str:
    """
    Verilen context ve soru için LLM'den cevap üretir.

    Args:
        context: İlgili doküman metinleri
        question: Kullanıcı sorusu

    Returns:
        LLM'in ürettiği cevap
    """
    llm = get_llm()
    prompt = get_prompt()
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response
