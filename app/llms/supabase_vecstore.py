from langchain_community.vectorstores.supabase import SupabaseVectorStore

from app.services.supabase import supabase as client


def get_vector_store(embedding, table_name: str) -> SupabaseVectorStore:
    return SupabaseVectorStore(
        client=client, table_name=table_name, embedding=embedding
    )
