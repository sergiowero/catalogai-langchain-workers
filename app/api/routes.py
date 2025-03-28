from fastapi import APIRouter, HTTPException
from models.requests import EmbeddingRequest
from services.queues import embeddings_queue_read
from usecases import embeddings_worker

router = APIRouter(prefix='/api/v1')


@router.post('/embeddings')
def generate_embedding(request: EmbeddingRequest):
    try:
        result = embeddings_worker.execute(request.items_to_process)

        return {'message': 'Embedding complete', 'result': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/queues/embeddings')
def get_embedding_queue_items():
    try:
        # Read from the queue
        items = embeddings_queue_read()

        if not items:
            raise HTTPException(
                status_code=404, detail='No embeddings items found in the queue'
            )

        return {'items': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
