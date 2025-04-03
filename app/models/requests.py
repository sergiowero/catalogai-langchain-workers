from typing import Any, Dict

from pydantic import BaseModel


class TaskRequest(BaseModel):
    """
    Base request model for all tasks.

    Attributes:
        parameters: Dict[str, Any] - Task-specific parameters
    """

    parameters: Dict[str, Any]
