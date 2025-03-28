import uuid
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


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


class ProductEmbedding(BaseModel):
    product_id: int
    content: str
    owner_id: uuid.UUID
    embedding: list[float] = Field(exclude=True)
    metadata: Optional[dict] = None
