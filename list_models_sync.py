import asyncio
from google import genai
import config

def test_models():
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    # Correct way to list models in new google-genai SDK
    models = client.models.list()
    for m in models:
        print(m.name)

test_models()
