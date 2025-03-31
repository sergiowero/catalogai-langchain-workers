from typing import Any, Callable, Dict

from pydantic import BaseModel


class TaskRunner(BaseModel):
    method: Callable
    params: Callable


class TaskRequest(BaseModel):
    """
    Base request model for all tasks.

    Attributes:
        parameters: Dict[str, Any] - Task-specific parameters
    """

    parameters: Dict[str, Any]


class EmbeddingTaskParameters(BaseModel):
    """
    Specific request model for embedding tasks.
    """

    items_to_process: int = 1
