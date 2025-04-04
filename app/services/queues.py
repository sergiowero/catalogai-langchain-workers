from app.models.queue import DatabaseQueueItem, EmbeddingQueueItem
from app.services.supabase import supabase_queues


def embeddings_queue_read(number: int) -> list[EmbeddingQueueItem]:
    """Read from the embeddings queue."""
    try:
        # Read from the queue
        rpc = supabase_queues.rpc(
            'read', {'queue_name': 'embeddings_jobs', 'sleep_seconds': 180, 'n': number}
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
        rpc = supabase_queues.rpc(
            'archive', {'queue_name': 'embeddings_jobs', 'message_id': id}
        )
        response = rpc.execute()
        return response
    except Exception as e:
        print(f'Error removing item from queue: {e}')
        return None


def database_events_queue_read(number: int) -> list[DatabaseQueueItem]:
    """Read from the event queue."""
    try:
        # Read from the queue
        rpc = supabase_queues.rpc(
            'read', {'queue_name': 'database_events', 'sleep_seconds': 180, 'n': number}
        )
        response = rpc.execute()
        return [DatabaseQueueItem.model_validate(item) for item in response.data]
    except Exception as e:
        print(f'Error reading from queue: {e}')
        return None


def database_events_queue_remove(msg_id: int) -> None:
    """Remove to the event queue."""
    try:
        # Write to the queue
        rpc = supabase_queues.rpc(
            'archive', {'queue_name': 'database_events', 'message_id': msg_id}
        )
        response = rpc.execute()
        return response
    except Exception as e:
        print(f'Error removing item from queue: {e}')
        return None
