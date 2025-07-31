"""
Base class for LLM providers.
"""

from abc import ABC, abstractmethod


class LLM(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt (str): The prompt to generate text from.
            **kwargs: Additional arguments to pass to the LLM provider.

        Returns:
            str: The generated text.
        """
        pass
