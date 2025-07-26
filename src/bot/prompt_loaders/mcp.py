"""
Button loader module for report ticket UI components.

This module defines a loader class responsible for registering and
unregistering interactive button components related to report tickets.
"""

from typing import List

from bot.core.command_center import handle_prompt_input
from bot.models.prompt import Prompt
from bot.ui.buttons.buttons_manager import ButtonsManager


class McpPromptLoader:
    """
    Loader for report ticket-related button components.

    Registers and unregisters all button views and their associated
    interaction handlers for report-related actions.
    """

    @staticmethod
    def load_prompts(prompts: List[Prompt]):
        """
        Register all prompt callbacks/views.
        """
        # register callbacks
        for prompt in prompts:
            ButtonsManager.register_callback(prompt.custom_id, handle_prompt_input)

    @staticmethod
    def unload_prompts(prompts: List[Prompt]):
        """
        Unregister all button callbacks/views.
        """
        # unregister callbacks
        for prompt in prompts:
            ButtonsManager.unregister_callback(prompt.custom_id)
