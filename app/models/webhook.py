from typing import Any

from pydantic import BaseModel, ConfigDict


class DatabaseWebhookPayload(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: str
    table: str
    record: dict[str, Any] | None
    old_record: dict[str, Any] | None
