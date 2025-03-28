import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Default to 'gemini' if not set
    ENABLE_IMAGE_CAPTIONS = (
        os.getenv('ENABLE_IMAGE_CAPTIONS', 'false').lower() == 'true'
    )


config = Config()
