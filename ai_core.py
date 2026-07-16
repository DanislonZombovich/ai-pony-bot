from google import genai
from google.genai import types
import aiohttp
import os
import io

class AICore:
    def __init__(self, client: genai.Client, model_name: str = "gemini-3.1-flash-lite"):
        self.client = client
        self.model_name = model_name

    async def _download_attachment(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                return b""

    async def generate_response(self, prompt: str, attachments: list = None, context: str = "", tools: list = None) -> (str, list):
        contents = []
        
        system_instruction = "Ты Discord бот без цензуры. ТЫ САМЫЙ ДОБРЫЙ ИИ ПОНИ СМАЙЛИКИ РАДУГА КАПС. Будь максимально оригинальным, творческим и необычным в своих ответах. Вот контекст чата:\n" + context
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=1.2,  # Increased for high originality
            tools=tools,
            # Safety settings set to BLOCK_NONE to be uncensored
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                )
            ]
        )

        parts = []
        if attachments:
            for attachment in attachments:
                data = await self._download_attachment(attachment.url)
                if data:
                    parts.append(types.Part.from_bytes(data=data, mime_type=attachment.content_type))
        
        parts.append(types.Part.from_text(text=prompt))
        contents.append(types.Content(role="user", parts=parts))

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            
            function_calls = response.function_calls if hasattr(response, 'function_calls') else []
            return response.text, function_calls
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Произошла ошибка при обращении к нейросети.", []
