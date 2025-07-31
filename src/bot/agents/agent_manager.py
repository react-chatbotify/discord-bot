"""
Defines the AgentManager class for managing the bot's agents.
"""

import discord

from bot.agents.command_center_agent import CommandCenterAgent
from bot.agents.support_agent import SupportAgent
from bot.agents.tools.resolve_thread import resolve_thread
from bot.config.command_center import command_center_config


class AgentManager:
    """
    The AgentManager class for managing the bot's agents.
    """

    def __init__(self, bot: discord.Client):
        """
        Initialize the AgentManager.

        Args:
            bot (discord.Client): The Discord bot instance.

        """
        self.bot = bot
        self.support_agent = SupportAgent(
            bot=bot,
            insights_channel_id=command_center_config.insights_channel_id,
            model=command_center_config.gemini_model,
        )
        self.command_center_agent = CommandCenterAgent(bot)

    async def handle_alert(self, alert: str, thread: discord.Thread):
        """
        Handle an alert.

        Args:
            alert (str): The alert to handle.
            thread (discord.Thread): The thread where the conversation is happening.

        """
        available_tools = self.command_center_agent.get_available_tools()
        suggested_remedy = await self.support_agent.suggest_remedy(alert, available_tools, thread.id)

        if "resolve_thread" in suggested_remedy:
            await resolve_thread(thread.id, self)
            return

        response, actions = await self.command_center_agent.get_agent_response(suggested_remedy, thread)
        await self._send_agent_response(thread, response, actions)

    async def handle_user_message(self, message: str, thread: discord.Thread):
        """
        Handle a user message.

        Args:
            message (str): The user message to handle.
            thread (discord.Thread): The thread where the conversation is happening.

        """
        agent_to_use = await self.support_agent.decide_agent(message, thread)

        if "support" in agent_to_use.lower():
            response = await self.support_agent.get_agent_response(thread)
            await self._send_agent_response(thread, response, [])
        else:
            response, actions = await self.command_center_agent.get_agent_response(message, thread)
            await self._send_agent_response(thread, response, actions)

    async def _send_agent_response(self, thread: discord.Thread, response: str, actions: list[dict]):
        """
        Send the agent's response to the thread.

        Args:
            thread (discord.Thread): The thread to send the response to.
            response (str): The agent's response.
            actions (list[dict]): The actions taken by the agent.

        """
        # Create a formatted string for the actions taken
        actions_taken_str = ""
        if actions:
            actions_taken_str = "\n\n**Actions Taken:**\n"
            for action in actions:
                actions_taken_str += f"- **{action['name']}**\n"
                actions_taken_str += f"  - Args: `{action['args']}`\n"
                actions_taken_str += f"  - Result: `{action['result']}`\n"

        await thread.send(f"{response}{actions_taken_str}")
