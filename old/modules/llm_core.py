# modules/llm_core.py
import os
from dotenv import load_dotenv

load_dotenv()

claude_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

class LLMEngine:
    def __init__(self):
        if claude_api_key:
            self.backend = "claude"
        elif openai_api_key:
            self.backend = "openai"
        else:
            self.backend = "local"

    def respond(self, context, role, message, emotion):
        if self.backend == "claude":
            return self._respond_claude(context, message)
        elif self.backend == "openai":
            return self._respond_openai(context, message)
        else:
            return self._respond_local(context, message)

    def _respond_claude(self, context, message):
        import requests
        headers = {
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        body = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 512,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": message}
            ]
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
        if response.status_code == 200:
            return response.json()["content"][0]["text"].strip()
        else:
            return f"[Claude error: {response.status_code}]"

    def _respond_openai(self, context, message):
        import openai
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()

    def _respond_local(self, context, message):
        return "I'm just a local dummy brain for now. Add an API key for cloud intelligence."
