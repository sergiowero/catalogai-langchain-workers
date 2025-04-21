from langchain.chat_models import init_chat_model
from langchain.llms.base import BaseLLM
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

cache = {}


def provide_llm(model: str, model_provider: str, temperature: float = 1.0) -> BaseLLM:
    """Get the LLM instance for the specified model, provider, and temperature."""
    cache_key = (model, model_provider, temperature)
    if cache_key in cache:
        return cache[cache_key]

    llm = init_chat_model(
        model=model, model_provider=model_provider, temperature=temperature
    )
    cache[cache_key] = llm
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


def provide_vector_store(
    vector_store_provider_name, embeddings_provider_name, table_name: str
) -> VectorStore:
    cache_key = (vector_store_provider_name, embeddings_provider_name, table_name)
    if cache_key in cache:
        return cache[cache_key]
    embeddings = get_embeddings(embeddings_provider_name)
    if vector_store_provider_name == 'supabase':
        from app.llms.supabase_vecstore import get_vector_store

        vector_store = get_vector_store(embeddings, table_name)
        cache[cache_key] = vector_store
        return vector_store
    else:
        raise ValueError(
            f'Unsupported vector store provider: {vector_store_provider_name}'
        )
