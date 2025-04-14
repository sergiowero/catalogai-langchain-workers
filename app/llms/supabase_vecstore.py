from langchain_community.vectorstores.supabase import SupabaseVectorStore
from services.supabase import supabase as client


def get_vector_store(embeddings):
    return SupabaseVectorStore(
        client=client, table_name='documents', embeddings=embeddings
    )
