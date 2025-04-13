"""
API Routes Module

This module defines the FastAPI routes for handling product embeddings and queue management.
It provides endpoints for generating embeddings and managing the embeddings queue.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError

from app.celeryapp import celery
from app.models.requests import TaskRequest
from app.services import captioning

router = APIRouter(prefix='/api/v1')


@router.post(
    '/tasks/{task_name}',
    summary='Execute a background task',
    description="""
    Execute a background task with the provided parameters.
    """,
    responses={
        200: {'description': 'Task created'},
        404: {'description': 'Task not found'},
        400: {'description': 'Invalid request parameters'},
        500: {'description': 'Internal server error'},
    },
)
def run_task(request: TaskRequest, task_name: str):
    """
    Execute a background task with the provided parameters.
    """
    try:
        res = celery.send_task(task_name, kwargs={'params': request.parameters})

        return {'status': res.state, 'task_name': task_name, 'task_id': res.id}
    except HTTPException as e:
        raise e
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CaptionTestRequest(BaseModel):
    image_url: str


@router.post('/test/caption', summary='Generate captions for images')
async def generate_captions(request: CaptionTestRequest):
    """
    Generate captions for the given images.
    """
    captions = captioning.get_image_caption(
        captioning.get_image_data(request.image_url)
    )
    return {
        'status': 'success',
        'message': 'Captions generated successfully',
        'data': captions,
    }
