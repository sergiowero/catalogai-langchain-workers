from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    items_to_process: int
