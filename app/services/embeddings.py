from langchain_core.documents import Document

from app.llms import provider
from app.models.embeddings import EmbeddingResult


def embed_documents(documents: list[Document]):
    """ """

    embeddings = provider.init_vector_store('supabase', 'google_genai')
    result = embeddings.add_documents(documents)

    return [EmbeddingResult(values=e.values) for e in result]
