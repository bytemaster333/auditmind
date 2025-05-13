import aiohttp
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

class OpenLLM:
    def __init__(self):
        self.api_key = os.getenv("ASI_API_TOKEN")
        self.base_url = "https://api.asi1.ai/v1/chat/completions"
        self.ssl_context = ssl._create_unverified_context()  # Sertifika doğrulamasını kapat

    async def complete(self, prompt: str, temperature: float = 0.2) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "asi1-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 500
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload, ssl=self.ssl_context) as response:
                if response.status != 200:
                    raise Exception(f"LLM Error {response.status}: {await response.text()}")
                result = await response.json()
                return result["choices"][0]["message"]["content"].strip()
