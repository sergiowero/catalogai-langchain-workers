from pydantic import BaseModel

from app.models.queue import EmbeddingQueueItem


class EmbeddingQueueResponse(BaseModel):
    items: list[EmbeddingQueueItem]
    queue_name: str
