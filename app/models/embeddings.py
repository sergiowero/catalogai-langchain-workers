from pydantic import BaseModel, ConfigDict


class EmbeddingResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    values: list[float]
