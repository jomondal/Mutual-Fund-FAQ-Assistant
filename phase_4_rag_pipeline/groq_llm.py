"""Groq LLM integration for response generation."""

from groq import Groq

from config.settings import settings


class GroqLLM:
    """Wrapper for Groq API calls."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.groq_api_key
        self.model = model or settings.groq_model
        self._client: Groq | None = None

    @property
    def client(self) -> Groq:
        if self._client is None:
            if not self.api_key:
                raise ValueError(
                    "GROQ_API_KEY not set. Copy .env.example to .env and add your key."
                )
            self._client = Groq(api_key=self.api_key)
        return self._client

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        """Generate a response using Groq chat completions."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=300,
        )
        return response.choices[0].message.content or ""
