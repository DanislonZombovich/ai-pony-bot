import re

with open("ai_core.py", "r") as f:
    code = f.read()

import_settings = """
import bot_settings

class AICore:
"""

code = code.replace("class AICore:", import_settings)

code = code.replace(
"""    def __init__(self, client: genai.Client, model_name: str = "gemini-3.1-flash-lite"):
        self.client = client
        self.model_name = model_name""",
"""    def __init__(self, client: genai.Client, model_name: str = bot_settings.TEXT_MODEL):
        self.client = client
        self.model_name = model_name"""
)

# Update parameters
code = code.replace(
"""        system_instruction = "Ты Discord бот без цензуры. ТЫ САМЫЙ ДОБРЫЙ ИИ ПОНИ СМАЙЛИКИ РАДУГА КАПС. Будь максимально оригинальным, творческим и необычным в своих ответах. Вот контекст чата:\\n" + context""",
"""        system_instruction = bot_settings.SYSTEM_INSTRUCTION + "\\n\\nВот контекст чата:\\n" + context"""
)
code = code.replace("temperature=1.2,", "temperature=bot_settings.TEMPERATURE,")

# The user wants multimodal support: images, documents, audio, videos.
# Gemini supports many mime types natively. However, files over ~20MB or certain formats might require the File API instead of inline data.
# For Discord attachments, most are <25MB, but video/audio is best uploaded via File API.
# Let's add upload logic using `self.client.aio.files.upload`.

upload_logic = """
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
"""

code = code.replace(
"""        parts = []
        if attachments:
            for attachment in attachments:
                data = await self._download_attachment(attachment.url)
                if data:
                    parts.append(types.Part.from_bytes(data=data, mime_type=attachment.content_type))""",
"""        parts = []
        if attachments:
            parts.extend(await self._process_attachments(attachments))"""
)

code = code.replace("class AICore:", upload_logic + "\nclass AICore:")

with open("ai_core.py", "w") as f:
    f.write(code)

print("Updated ai_core.py with proper File API usage")
