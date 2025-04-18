import uuid
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.services.supabase import supabase


class Product(BaseModel):
    id: int
    owner_id: uuid.UUID
    source_id: Optional[str] = None
    url: Optional[HttpUrl] = None
    name: str
    description: Optional[str] = None
    image_urls: Optional[list[HttpUrl]] = None
    metadata: Optional[dict] = None
    price: Optional[float] = None

    @staticmethod
    def fetchById(id: int) -> 'Product':
        response = (
            supabase.table('products')
            .select('*')
            .eq('id', id)
            .limit(1)
            .single()
            .execute()
        )
        return Product.model_validate(response.data)


class ProductEmbeddingData(BaseModel):
    product_id: int
    content: str
    owner_id: uuid.UUID
    embedding: list[float] | None = Field(exclude=True)
    metadata: Optional[dict] = None


class ProductEmbedding(ProductEmbeddingData):
    id: int

    @staticmethod
    def insert(product_embedding: ProductEmbeddingData):
        response = (
            supabase.table('product_documents')
            .insert(product_embedding.model_dump(mode='json'))
            .execute()
        )
        return ProductEmbedding.model_validate(response.data[0])

    def fetchMany(ids: list[int]):
        response = (
            supabase.table('product_documents').select('*').in_('id', ids).execute()
        )
        return [ProductEmbedding.model_validate(data) for data in response.data]

    def updateContent(data: list[dict]):
        response = (
            supabase.table('product_documents')
            .upsert([{'id': e['id'], 'embedding': e['embedding']} for e in data])
            .execute()
        )
        return [ProductEmbedding.model_validate(data) for data in response.data]


class ProductCaptions(BaseModel):
    product_id: int
    image_url_hash: int
    owner_id: uuid.UUID
    captions: str
    metadata: dict | None = None

    @staticmethod
    def insert(product_caption: 'ProductCaptions') -> 'ProductCaptions':
        response = (
            supabase.table('product_captions')
            .upsert(product_caption.model_dump(mode='json'))
            .execute()
        )
        return ProductCaptions.model_validate(response.data[0])
