from enum import Enum

from pydantic import BaseModel

from models.product import Product


class JobStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class EmbeddingQueueMessage(BaseModel):
    job_id: int
    product: Product


class EmbeddingQueueItem(BaseModel):
    msg_id: int
    message: EmbeddingQueueMessage
