"""
This module defines the UI view for suggesting prompts to the user.
"""

import discord

from bot.models.prompt import Prompt


class PromptSuggestionsView(discord.ui.View):
    """
    A view that displays prompt suggestions in a dropdown menu.
    """

    def __init__(self, prompts: list[Prompt]):
        super().__init__()

        options = [
            discord.SelectOption(label=prompt.content, value=prompt.title) for prompt in prompts
        ]
        self.add_item(
            discord.ui.Select(
                placeholder="Choose a prompt",
                options=options,
                custom_id="prompt_suggestion_select",
            )
        )
