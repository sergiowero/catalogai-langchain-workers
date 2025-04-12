from langchain.llms.base import BaseLLM
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

DEFAULT_EMBEDDING_MODEL = 'text-embedding-004'
DEFAULT_MODEL = 'gemini-2.0-flash'


def create_embeddings() -> Embeddings:
    return GoogleGenerativeAIEmbeddings(
        model=DEFAULT_EMBEDDING_MODEL, task_type='retrieval_document'
    )


def create_llm() -> BaseLLM:
    return GoogleGenerativeAI(model=DEFAULT_MODEL)


def create_chat() -> BaseChatModel:
    return ChatGoogleGenerativeAI(model=DEFAULT_MODEL)
