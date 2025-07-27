"""
Prompt loader module for mcp components.

This module defines a loader class responsible for mcp prompts.
"""

from typing import List

from bot.core.command_center import handle_prompt_input
from bot.models.prompt import Prompt
from bot.ui.prompts.prompts_manager import PromptsManager


class McpPromptLoader:
    """
    Loader for mcp-related prompt components.

    Registers and unregisters all prompt views and their associated
    interaction handlers for mcp-related actions.
    """

    @staticmethod
    def load_prompts(prompts: List[Prompt]):
        """
        Register all prompt callbacks/views.
        """
        # register callbacks
        for prompt in prompts:
            PromptsManager.register_callback(prompt.custom_id, prompt.content, handle_prompt_input)

    @staticmethod
    def unload_prompts(prompts: List[Prompt]):
        """
        Unregister all prompt callbacks/views.
        """
        # unregister callbacks
        for prompt in prompts:
            PromptsManager.unregister_callback(prompt.custom_id)
