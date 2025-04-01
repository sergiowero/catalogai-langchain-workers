from pydantic import BaseModel

from models.queue import EmbeddingQueueItem


class EmbeddingQueueResponse(BaseModel):
    items: list[EmbeddingQueueItem]
    queue_name: str
