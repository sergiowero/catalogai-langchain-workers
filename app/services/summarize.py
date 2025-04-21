from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llms import provider
from app.models.product import Product
from app.prompts import product_marketing, product_rag
from app.services.supabase import supabase

messages_rag = [
    ('system', product_rag.SYSTEM_PROMPT),
    ('human', product_rag.HUMAN_PROMPT),
]

messages_marketing = [
    ('system', product_marketing.SYSTEM_PROMPT),
    ('human', product_marketing.HUMAN_PROMPT),
]

prompt_rag = ChatPromptTemplate.from_messages(messages_rag)
prompt_marketing = ChatPromptTemplate.from_messages(messages_marketing)

output_parser = StrOutputParser()


def generate_rag_description(product: Product):
    metadata_text = ', '.join(
        f'{key}: {value}' for key, value in product.metadata.items()
    )

    llm = provider.provide_llm(
        model='gemini-2.0-flash', model_provider='google_genai', temperature=1
    )

    chain = prompt_rag | llm | output_parser
    response = chain.invoke({**product.model_dump(), 'metadata': metadata_text})

    return response


def sumarize_marketing_description(description: str, product: Product):
    llm = provider.provide_llm(
        model='gemini-2.0-flash', model_provider='google_genai', temperature=1
    )

    chain = prompt_marketing | llm | output_parser
    response = chain.invoke({**product.model_dump(), 'description': description})

    return response


def upsert_sumarize_results(rag: str, marketing: str, product: Product):
    """
    Save the results of the summarization to the database.
    """
    vector_store = provider.provide_vector_store(
        vector_store_provider_name='supabase',
        embeddings_provider_name='google_genai',
        table_name='product_documents',
    )

    docuement = Document(
        page_content=rag,
        metadata={
            'product_id': product.id,
            'owner_id': str(product.owner_id),
            'marketing_description': marketing,
        },
    )

    supabase.table('product_documents').delete().eq(
        'metadata->product_id', product.id
    ).execute()

    vector_store.add_documents([docuement])
