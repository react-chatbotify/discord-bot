"""
AgentsCog module for managing the bot's agents.
"""

from discord.ext import commands

from bot.agents.agent_manager import AgentManager
from bot.utils.console_logger import console_logger

class AgentsCog(commands.Cog):
    """
    A cog for managing the bot's agents.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the AgentsCog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot
        self.agent_manager = AgentManager(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event listener for when the bot is ready.
        """
        try:
            await self.agent_manager.command_center_agent.load_all_prompts()
            console_logger.info("✅ Prompts loaded successfully.")
        except Exception as e:
            console_logger.error(f"❌ Failed to load prompts: {e}")

        try:
            await self.agent_manager.command_center_agent.set_system_context()
            console_logger.info("✅ System context set successfully.")
        except Exception as e:
            console_logger.error(f"❌ Failed to set system context: {e}")


async def setup(bot: commands.Bot):
    """
    Set up the AgentsCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.
    """
    await bot.add_cog(AgentsCog(bot))
