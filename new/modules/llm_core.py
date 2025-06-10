import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self, model_name="claude-3-haiku-20240307"):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model_name = model_name

    def respond(self, context, vision_desc, speech, mood):
        prompt = f"""
        [Vision]: {vision_desc}
        [Speech]: {speech}
        [Mood]: {mood}
        [Memory]: {context}
        Response:
        """

        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()