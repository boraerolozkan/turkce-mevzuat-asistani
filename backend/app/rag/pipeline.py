from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from app.rag.embeddings import get_embeddings
from app.rag.retriever import get_retriever
from app.rag.generator import get_llm, get_prompt


def format_docs(docs):
    """
    Doküman listesini tek bir string'e çevirir.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain():
    """
    Tam RAG pipeline'ını döndürür.

    Pipeline:
    1. Kullanıcı sorusu alınır
    2. Retriever ile ilgili dokümanlar getirilir
    3. Dokümanlar ve soru LLM'e gönderilir
    4. Cevap ve kaynaklar birlikte döndürülür
    """
    retriever = get_retriever()
    llm = get_llm()
    prompt = get_prompt()

    # Context ve soruyu paralel işle
    rag_chain_from_docs = (
        RunnableParallel({
            "context": lambda x: x,
            "question": RunnablePassthrough()
        })
        | prompt
        | llm
        | StrOutputParser()
    )

    # Retriever'dan gelen context ile birleştir
    rag_chain_with_source = RunnableParallel({
        "context": retriever,
        "question": RunnablePassthrough()
    }).assign(answer=rag_chain_from_docs)

    return rag_chain_with_source


def ask_question(question: str) -> dict:
    """
    Kullanıcı sorusunu işleyip cevap ve kaynakları döndürür.

    Args:
        question: Kullanıcı sorusu

    Returns:
        {
            "answer": "...",
            "context": [Document, ...]
        }
    """
    chain = get_rag_chain()
    result = chain.invoke(question)
    return result
