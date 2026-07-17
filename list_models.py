import asyncio
from google import genai
import config

async def test_live():
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    # In older / different genai SDKs, it's models.list_models() but we can try client.models.list()
    # Actually, we know that Bidi / Live requires Gemini 2.0.
    # In google-genai 0.2.0 (which is installed), the correct string might be just "gemini-2.0-flash-exp"
    # Wait, earlier I used model="models/gemini-2.0-flash-exp" maybe? Let's check test output.
    try:
        models = client.models.list_models()
        for m in models:
            if "2.0" in m.name:
                print(m.name)
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(test_live())
