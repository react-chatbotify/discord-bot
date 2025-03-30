"""
Admin command processing module for module listing and slash command sync.

This module provides utility functions used by admin-level commands for
managing the bot’s modules and synchronizing slash commands with
Discord’s API. It includes functions for listing currently loaded
extensions and triggering per-guild command syncs.
"""

import discord
from discord.ext import commands

from bot.cogs.cogs_manager import CogsManager


async def process_list_modules(interaction: discord.Interaction, bot: commands.Bot, cogs_manager: CogsManager):
    """
    List all bot modules and their current enabled/disabled status.

    Args:
        interaction (discord.Interaction): The interaction that triggered the command.
        bot (commands.Bot): The Discord bot instance.
        cogs_manager (CogsManager): The cogs manager instance to access available modules.

    """
    # Get list of loaded extensions
    loaded_cogs = list(bot.extensions.keys())
    parsed_loaded_cogs = list(map(lambda name: name.split('.')[-1], loaded_cogs))

    # Get list of all available cogs from the manager
    available_cogs = cogs_manager.cogs

    # Format the message
    message = "**📋 Module Status:**\n\n"

    for cog_name in available_cogs:
        status = "✅ Enabled" if cog_name in parsed_loaded_cogs else "❌ Disabled"
        message += f"• **{cog_name}**: {status}\n"

    # Add total count
    message += f"\n**Total:** {len(loaded_cogs)}/{len(available_cogs)} modules enabled"

    await interaction.response.send_message(message, ephemeral=True)


async def process_sync_commands(ctx: commands.Context):
    """
    Sync slash commands with Discord's API for this guild only.

    This function clears outdated commands, copies global commands into the guild,
    and performs a sync to register them with Discord. It is designed to run per-guild
    and will show a success or error message upon completion.

    Args:
        ctx (commands.Context): The command context used to respond and access the bot.

    """
    await ctx.defer(ephemeral=True)

    try:
        bot: commands.Bot = ctx.bot
        guild = ctx.guild

        # 1️⃣ Clear old commands before resyncing
        bot.tree.clear_commands(guild=guild)

        # 2️⃣ Copy global commands to this guild
        bot.tree.copy_global_to(guild=guild)

        # 3️⃣ Sync commands to ensure old ones are gone
        await bot.tree.sync(guild=guild)

        # 4️⃣ Get the updated count and send success message
        command_count = len(bot.tree.get_commands(guild=guild))
        await ctx.send(
            f"✅ Successfully synced {command_count} commands to {guild.name}.",
            ephemeral=True,
        )

    except discord.errors.HTTPException as e:
        await ctx.send(
            f"❌ Error syncing commands: {e}. You may have hit a rate limit.",
            ephemeral=True,
        )
