with open("ai_core.py", "r") as f:
    code = f.read()

# Add retry logic for 503 Service Unavailable using tenacity
new_import = "from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type\nfrom google.api_core.exceptions import ServiceUnavailable, InternalServerError"
code = new_import + "\n" + code

retry_decorator = """
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
"""

code = code.replace("class AICore:", "class AICore:\n" + retry_decorator)

code = code.replace(
"""            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )""",
"            response = await self._generate_content_with_retry(contents, config)"
)

# And if error occurs we shouldn't just say error if it's 503 after retries
code = code.replace(
"""            print(f"Error generating content: {e}")
            return "Произошла ошибка при обращении к нейросети.", []""",
"""            print(f"Error generating content: {e}")
            if "503" in str(e) or "Service Unavailable" in str(e):
                return "Сейчас я очень перегружена запросами, подожди немного, мой босс! 🦄", []
            return "Произошла ошибка при обращении к нейросети.", []"""
)

with open("ai_core.py", "w") as f:
    f.write(code)

print("Updated ai_core.py")
