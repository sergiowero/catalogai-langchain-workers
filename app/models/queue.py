from typing import Any

from pydantic import BaseModel, ConfigDict


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


class DatabaseWebhookPayload(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: str
    table: str
    schema: str
    record: dict[str, Any] | None
    old_record: dict[str, Any] | None
