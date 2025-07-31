"""
Gemini LLM provider.
"""

from google import genai
from google.genai.types import GenerateContentResponse

from bot.llm.base import LLM


class Gemini(LLM):
    """
    Gemini LLM provider.
    """

    def __init__(self, model_name: str):
        """
        Initialize the Gemini LLM provider.

        Args:
            model_name (str): The name of the Gemini model to use.
        """
        self.model = genai.GenerativeModel(model_name)

    async def generate_text(self, prompt: str, **kwargs) -> GenerateContentResponse:
        """
        Generate text from a prompt.

        Args:
            prompt (str): The prompt to generate text from.
            **kwargs: Additional arguments to pass to the LLM provider.

        Returns:
            str: The generated text.
        """
        history = kwargs.get("history", [])
        tools = kwargs.get("tools", [])
        system_instruction = kwargs.get("system_instruction", "")

        chat = self.model.start_chat(history=history)
        return await chat.send_message_async(
            prompt,
            tools=tools,
            system_instruction=system_instruction,
        )
