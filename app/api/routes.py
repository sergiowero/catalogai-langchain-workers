"""
API Routes Module

This module defines the FastAPI routes for handling product embeddings and queue management.
It provides endpoints for generating embeddings and managing the embeddings queue.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.requests import TaskRequest
from pydantic import ValidationError
from tasks.product import embeddings
from tasks.queues import database_events

router = APIRouter(prefix='/api/v1')

task_runners = {
    'product-embeddings': embeddings.run,
    'process-database-event-queue': database_events,
}


@router.post(
    '/tasks/{task_id}/run',
    summary='Execute a background task',
    description="""
    Execute a background task with the provided parameters.
    """,
    responses={
        404: {'description': 'Task not found'},
        400: {'description': 'Invalid request parameters'},
        500: {'description': 'Internal server error'},
    },
)
def run_task(request: TaskRequest, task_id: str, background_tasks: BackgroundTasks):
    """
    Execute a background task with the provided parameters.
    """
    try:
        task_func = task_runners.get(task_id)

        if not task_func:
            raise HTTPException(status_code=404, detail='Task not found')

        background_tasks.add_task(task_func, request.parameters)

        return {'message': 'Task started', 'task_id': task_id}
    except HTTPException as e:
        raise e
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
