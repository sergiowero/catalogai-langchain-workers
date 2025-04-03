from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict

from models.product import Product



class EmbeddingQueueMessage(BaseModel):
    job_id: int
    product: Product


class EmbeddingQueueItem(BaseModel):
    msg_id: int
    message: EmbeddingQueueMessage


class DatabaseQueueMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: str
    table: str
    row_id: int
    prev: dict[str, Any] | None
    curr: dict[str, Any]


class DatabaseQueueItem(BaseModel):
    msg_id: int
    message: DatabaseQueueMessage
