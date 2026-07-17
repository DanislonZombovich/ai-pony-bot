from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from google import genai
from google.genai import types
import aiohttp
import os
import io


import bot_settings

class AICore:

    async def _process_attachments(self, attachments):
        parts = []
        for att in attachments:
            try:
                # Video and Audio are usually better uploaded to the File API if they are large,
                # but google-genai supports direct byte parts for some, however file API is safer.
                data = await self._download_attachment(att.url)
                if data:
                    if att.content_type and (att.content_type.startswith('video/') or att.content_type.startswith('audio/')):
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=att.filename) as tmp:
                            tmp.write(data)
                            tmp_name = tmp.name
                        
                        # Upload using File API
                        # `client.aio.files.upload` is correct for google-genai
                        uploaded_file = await self.client.aio.files.upload(file=tmp_name, config={'mime_type': att.content_type})
                        parts.append(uploaded_file)
                        os.unlink(tmp_name)
                    else:
                        mime = att.content_type or "application/octet-stream"
                        parts.append(types.Part.from_bytes(data=data, mime_type=mime))
            except Exception as e:
                print(f"Attachment error: {e}")
        return parts

class AICore:


    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=30), 
        stop=stop_after_attempt(5),
        reraise=True
    )
    async def _generate_content_with_retry(self, contents, config):
        return await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config
        )

    def __init__(self, client: genai.Client, model_name: str = bot_settings.TEXT_MODEL):
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
        
        system_instruction = bot_settings.SYSTEM_INSTRUCTION + "\n\nВот контекст чата:\n" + context
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=bot_settings.TEMPERATURE,  # Increased for high originality
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
            parts.extend(await self._process_attachments(attachments))
        
        parts.append(types.Part.from_text(text=prompt))
        contents.append(types.Content(role="user", parts=parts))

        try:
            response = await self._generate_content_with_retry(contents, config)
            
            function_calls = response.function_calls if hasattr(response, 'function_calls') else []
            return response.text, function_calls
            
        except Exception as e:
            print(f"Error generating content: {e}")
            if "503" in str(e) or "Service Unavailable" in str(e):
                return "Сейчас я очень перегружена запросами, подожди немного, мой босс! 🦄", []
            return "Произошла ошибка при обращении к нейросети.", []
