"""
Defines the InsightAgent class for processing and consolidating insights from Discord channels.
"""

import discord

from bot.llm.gemini import Gemini
from bot.utils.console_logger import console_logger


class SupportAgent:
    """
    The SupportAgent class for processing and consolidating insights from Discord channels.
    """

    def __init__(self, bot: discord.Client, insights_channel_id: int, model: str):
        """
        Initialize the SupportAgent.

        Args:
            bot (discord.Client): The Discord bot instance.
            insights_channel_id (int): The ID of the channel where insights are stored.
            model (str): The name of the Gemini model to use.

        """
        self.bot = bot
        self.insights_channel_id = insights_channel_id
        self.llm = Gemini(model)

    async def get_insights_from_thread(self, thread: discord.Thread) -> str:
        """
        Get insights from a Discord thread.

        Args:
            thread (discord.Thread): The thread to get insights from.

        Returns:
            str: A summary of the key takeaways from the thread.

        """
        messages = []
        async for msg in thread.history(limit=None):
            messages.append(msg.content)

        # Reverse the messages to have the oldest message first
        messages.reverse()

        # Join the messages into a a single string
        thread_content = "\n".join(messages)

        # Use an LLM to summarize the key takeaways
        return await self.llm.generate_text(
            f"Summarize the key takeaways from the following conversation:\n{thread_content}"
        )

    async def update_insights_channel(self, insights: str):
        """
        Update the insights channel with the new insights.

        Args:
            insights (str): The new insights to post to the channel.

        """
        channel = self.bot.get_channel(self.insights_channel_id)
        if not channel:
            console_logger.error(f"Could not find insights channel with ID {self.insights_channel_id}")
            return

        await channel.send(insights)

    async def get_insights_from_channel(self) -> str:
        """
        Get the most recent insights from the insights channel.

        Returns:
            str: The most recent insights from the insights channel.

        """
        channel = self.bot.get_channel(self.insights_channel_id)
        if not channel:
            console_logger.error(f"Could not find insights channel with ID {self.insights_channel_id}")
            return ""

        async for message in channel.history(limit=1):
            return message.content

        return ""

    async def suggest_remedy(self, alert: str, available_tools: list[str], thread_id: int) -> str:
        """
        Suggest a remedy for an alert.

        Args:
            alert (str): The alert to suggest a remedy for.
            available_tools (list[str]): The tools available to the command center agent.
            thread_id (int): The ID of the thread where the conversation is happening.

        Returns:
            str: A suggested course of action.

        """
        insights = await self.get_insights_from_channel()

        return await self.llm.generate_text(
            f"Given the following alert:\n{alert}\n\nAnd the following available tools:\n{', '.join(available_tools)}\n\nAnd the following insights from previous conversations:\n{insights}\n\nWhat is the best course of action to take? If you believe the issue has been resolved, you can use the `resolve_thread` tool to close the thread and learn from the conversation. You can call the tool by responding with `resolve_thread(thread_id={thread_id})`."
        )

    async def decide_agent(self, message: str, thread: discord.Thread) -> str:
        """
        Decide which agent should handle the user's message.

        Args:
            message (str): The user's message.
            thread (discord.Thread): The thread where the conversation is happening.

        Returns:
            str: The name of the agent to use.

        """
        history = await self._get_thread_history(thread)
        return await self.llm.generate_text(
            f"Given the following conversation history:\n{history}\n\nAnd the following user message:\n{message}\n\nShould the support agent or the command center agent handle this message? The support agent is good at summarizing conversations and providing insights. The command center agent is good at executing commands and interacting with the MCP server. Respond with 'support' or 'command_center'."
        )

    async def get_agent_response(self, thread: discord.Thread) -> str:
        """
        Get the support agent's response.

        Args:
            thread (discord.Thread): The thread where the conversation is happening.

        Returns:
            str: The support agent's response.

        """
        return await self.get_insights_from_thread(thread)

    async def _get_thread_history(self, thread: discord.Thread) -> str:
        """
        Get the thread history as a string.

        Args:
            thread (discord.Thread): The thread to get the history from.

        Returns:
            str: The thread history as a string.

        """
        messages = []
        async for msg in thread.history(limit=None):
            messages.append(f"{msg.author.name}: {msg.content}")

        # Reverse the messages to have the oldest message first
        messages.reverse()

        return "\n".join(messages)
