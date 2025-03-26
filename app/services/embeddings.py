from langchain_community.embeddings import GooglePalmEmbeddings
from supabase import create_client, Client
from config import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def create_embedding(text: str):
    embedding_model = GooglePalmEmbeddings()
    embedding = embedding_model.embed(text)
    return embedding

def save_embedding_to_supabase(embedding: list, metadata: dict):
    data = {
        "embedding": embedding,
        "metadata": metadata
    }
    response = supabase.table("embeddings").insert(data).execute()
    return response