import uuid
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl
from services.supabase import supabase


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
        response = supabase.table('products').select('*').eq('id', id).execute()

        return Product.model_validate(response.data[0])


class ProductEmbedding(BaseModel):
    product_id: int
    content: str
    owner_id: uuid.UUID
    embedding: list[float] | None = Field(exclude=True)
    metadata: Optional[dict] = None

    @staticmethod
    def insert(product_embedding: 'ProductEmbedding'):
        supabase.table('product_embeddings').insert(
            product_embedding.model_dump(mode='json')
        ).execute()
