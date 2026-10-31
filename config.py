import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "862759084200558609"))

# Neon Serverless PostgreSQL connection string (supports legacy AIVEN_URI fallback)
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("AIVEN_URI") or ""
AIVEN_URI = DATABASE_URL
