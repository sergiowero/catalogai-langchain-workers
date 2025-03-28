from config import config
from models.queue import EmbeddingQueueItem
from supabase import Client, create_client
from supabase.client import ClientOptions

options = ClientOptions('pgmq_public')
queues: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY, options)


def embeddings_queue_read(number: int) -> list[EmbeddingQueueItem]:
    """Read from the embeddings queue."""
    try:
        # Read from the queue
        rpc = queues.rpc(
            'read', {'queue_name': 'embeddings_jobs', 'sleep_seconds': 60, 'n': number}
        )
        response = rpc.execute()
        return [EmbeddingQueueItem.model_validate(item) for item in response.data]
    except Exception as e:
        print(f'Error reading from queue: {e}')
        return None


def embeddings_queue_remove(id: int) -> None:
    """Write to the embeddings queue."""
    try:
        # Write to the queue
        rpc = queues.rpc('archive', {'queue_name': 'embeddings_jobs', 'message_id': id})
        response = rpc.execute()
        return response
    except Exception as e:
        print(f'Error removing item from queue: {e}')
        return None
