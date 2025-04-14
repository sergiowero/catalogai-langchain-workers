from langchain.llms.base import BaseLLM
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

cache = {}


def get_llm(provider_name) -> BaseLLM:
    """Get the LLM instance for the specified provider."""
    if provider_name in cache:
        return cache[provider_name]

    if provider_name == 'google_genai':
        from app.llms.google_genai import create_llm
    else:
        raise ValueError(f'Unsupported provider: {provider_name}')

    llm = create_llm()
    cache[provider_name] = llm
    return llm


def get_embeddings(provider_name) -> Embeddings:
    """Get the Embeddings instance for the specified provider."""
    if provider_name in cache:
        return cache[provider_name]

    if provider_name == 'google_genai':
        from app.llms.google_genai import create_embeddings
    else:
        raise ValueError(f'Unsupported provider: {provider_name}')

    embeddings = create_embeddings()
    cache[provider_name] = embeddings
    return embeddings


def get_vector_store(store_provider_name, embeddings_provider_name) -> VectorStore:
    embeddings = get_embeddings(embeddings_provider_name)
    if store_provider_name == 'supabase':
        from app.llms.supabase_vecstore import get_vector_store

        return get_vector_store(embeddings)
    else:
        raise ValueError(f'Unsupported vector store provider: {store_provider_name}')
