from config import config
from supabase import Client, create_client

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
