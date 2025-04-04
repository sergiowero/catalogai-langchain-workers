from supabase import Client, create_client
from supabase.client import ClientOptions

from app.config import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

options = ClientOptions('pgmq_public')
supabase_queues: Client = create_client(
    config.SUPABASE_URL, config.SUPABASE_KEY, options
)
