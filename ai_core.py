import os
import aiohttp
from google import genai
from google.genai import types

import bot_settings

class AICore:
    def __init__(self, client: genai.Client, model_name: str = None):
        self.client = client
        self.model_name = model_name or bot_settings.TEXT_MODEL
        self.fallback_models = getattr(bot_settings, "FALLBACK_MODELS", [])

    async def _download_attachment(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                return b""

    async def _process_attachments(self, attachments):
        parts = []
        for att in attachments:
            try:
                data = await self._download_attachment(att.url)
                if data:
                    if att.content_type and (att.content_type.startswith('video/') or att.content_type.startswith('audio/')):
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=att.filename) as tmp:
                            tmp.write(data)
                            tmp_name = tmp.name

                        uploaded_file = await self.client.aio.files.upload(
                            file=tmp_name,
                            config={'mime_type': att.content_type}
                        )
                        parts.append(uploaded_file)
                        try:
                            os.unlink(tmp_name)
                        except OSError:
                            pass
                    else:
                        mime = att.content_type or "application/octet-stream"
                        parts.append(types.Part.from_bytes(data=data, mime_type=mime))
            except Exception as e:
                print(f"Attachment error: {e}")
        return parts

    async def generate_response(self, prompt: str, attachments: list = None, context: str = "", tools: list = None) -> tuple:
        contents = []

        system_instruction = bot_settings.SYSTEM_INSTRUCTION
        if context:
            system_instruction += "\n\nВот контекст чата:\n" + context

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=bot_settings.TEMPERATURE,
            tools=tools,
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

        models_to_try = [self.model_name] + [m for m in self.fallback_models if m != self.model_name]

        last_error = None
        for model in models_to_try:
            try:
                response = await self.client.aio.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )

                function_calls = getattr(response, "function_calls", None)
                if not function_calls and hasattr(response, "candidates") and response.candidates:
                    # Some SDK versions have function_calls under candidate parts
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        function_calls = [p.function_call for p in candidate.content.parts if getattr(p, "function_call", None)]

                return response.text or "", function_calls or []

            except Exception as e:
                print(f"Model {model} failed: {e}. Trying fallback...")
                last_error = e

        print(f"All models exhausted. Last error: {last_error}")
        if last_error and ("503" in str(last_error) or "Service Unavailable" in str(last_error)):
            return "Сейчас я очень перегружена запросами, подожди немного, мой босс! 🦄", []
        return "Произошла ошибка при обращении к нейросети.", []
