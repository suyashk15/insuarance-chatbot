import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite+aiosqlite:///./insurance.db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

