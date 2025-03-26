from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    LANGCHAIN_MODEL = os.getenv("LANGCHAIN_MODEL", "gemini")  # Default to 'gemini' if not set

config = Config()