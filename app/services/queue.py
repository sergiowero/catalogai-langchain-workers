from supabase import create_client, Client
from supabase.client import ClientOptions

from config import config

options = ClientOptions("pgmq_public")
queues: Client = create_client(
    config.SUPABASE_URL, 
    config.SUPABASE_KEY, 
    options)

def queue_read():
    """Read from the queue."""
    try:
        # Read from the queue
        rpc = queues.rpc('read', {
            "queue_name": "embeddings_jobs",
            "sleep_seconds": 60,
            "n": 10
        })
        response = rpc.execute()
        return response.data
    except Exception as e:
        print(f"Error reading from queue: {e}")
        return None