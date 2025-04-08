from google.genai import types

from app.clients.gemini import DEFAULT_EMBEDDING_MODEL, client
from app.models.embeddings import Embedding


def generate_embedding(contents: list[str]):
    """
    Genera un embedding para el texto usando Gemini
    """

    result = client.models.embed_content(
        model=DEFAULT_EMBEDDING_MODEL,
        contents=contents,
        config=types.EmbedContentConfig(
            task_type='RETRIEVAL_DOCUMENT', output_dimensionality=768
        ),
    )

    return [Embedding(values=e.values) for e in result.embeddings]
