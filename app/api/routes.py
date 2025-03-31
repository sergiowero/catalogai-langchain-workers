"""
API Routes Module

This module defines the FastAPI routes for handling product embeddings and queue management.
It provides endpoints for generating embeddings and managing the embeddings queue.

Endpoints:
    - POST /embeddings: Generate embeddings for product data
    - GET /queues/embeddings: Retrieve items from the embeddings queue
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.task import TaskRequest, TaskRunner
from pydantic import ValidationError
from services.queues import embeddings_queue_read
from tasks import product_embeddings

router = APIRouter(prefix='/api/v1')

task_runners = {
    'product-embeddings': TaskRunner(
        method=product_embeddings.run, params=product_embeddings.validate_params
    )
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


@router.get('/queues/embeddings')
def get_embedding_queue_items():
    """
    Retrieve items from the embeddings queue.

    Returns:
        dict: Response containing the queue items

    Raises:
        HTTPException: If no items are found in the queue or if there's an error
    """
    try:
        items = embeddings_queue_read()

        if not items:
            raise HTTPException(
                status_code=404, detail='No embeddings items found in the queue'
            )

        return {'items': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
