"""
API Routes Module

This module defines the FastAPI routes for handling product embeddings and queue management.
It provides endpoints for generating embeddings and managing the embeddings queue.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from models.responses import EmbeddingQueueResponse
from models.task import TaskRequest, TaskRunner
from pydantic import ValidationError
from services.queues import embeddings_queue_read
from tasks import product_embeddings

router = APIRouter(prefix='/api/v1')

task_runners = {
    'product-embeddings': TaskRunner(
        method=product_embeddings.run, params=product_embeddings.validate_params
    ),
    'handle-event-queue': TaskRunner(method=lambda _: None, params=lambda _: _),
}


@router.post('/tasks/{task_id}/run')
def run_task(request: TaskRequest, task_id: str, background_tasks: BackgroundTasks):
    """
    Execute a background task with the provided parameters.

    Args:
        request (TaskRequest): Request containing task parameters
            - parameters: Dict[str, Any] - Task-specific parameters
        task_id (str): ID of the task to execute
        background_tasks (BackgroundTasks): FastAPI background tasks object

    Returns:
        dict: Response indicating the task has started
            - message: str - Status message
            - task_id: str - ID of the executed task

    Raises:
        HTTPException:
            - 404: If the task is not found
            - 400: If there's a validation error in the request parameters
            - 500: If there's an error executing the task
    """
    try:
        task = task_runners.get(task_id)

        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        background_tasks.add_task(task.method, task.params(request.parameters))

        return {'message': 'Task started', 'task_id': task_id}
    except HTTPException as e:
        raise e
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    '/queues/embeddings',
    summary='Retrieve items from the embeddings queue',
    description='Get a specified number of items from the embeddings queue. Useful for monitoring and debugging queue operations.',
    response_description='List of embeddings queue items',
    responses={
        404: {'description': 'No embeddings items found in the queue'},
        500: {'description': 'Internal server error'},
    },
)
def get_embedding_queue_items(
    number: int = Query(
        default=10,
        description='Number of items to retrieve from the queue',
        ge=1,  # minimum value
        le=100,  # maximum value
    ),
) -> EmbeddingQueueResponse:
    """
    Retrieve items from the embeddings queue.
    """
    try:
        items = embeddings_queue_read(number)

        if not items:
            raise HTTPException(
                status_code=404, detail='No embeddings items found in the queue'
            )

        return {'items': items, 'queue_name': 'embedding_jobs'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
