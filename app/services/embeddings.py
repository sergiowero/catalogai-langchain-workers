from google import genai
from google.genai import types

from app.models.embeddings import Embedding

client = genai.Client()

DEFAULT_MODEL = 'text-embedding-004'


def generate_embedding(contents: list[str]):
    """
    Genera un embedding para el texto usando Gemini
    """

    result = client.models.embed_content(
        model=DEFAULT_MODEL,
        contents=contents,
        config=types.EmbedContentConfig(
            task_type='RETRIEVAL_DOCUMENT', output_dimensionality=768
        ),
    )

    return [Embedding(values=e.values) for e in result.embeddings]
