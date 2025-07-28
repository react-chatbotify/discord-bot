"""
Core module for handling alerts received from webhook.

This module processes alerts and determines further actions.
"""

import discord
from discord.ext import commands

from bot.agents.instructions import AGENT_INSTRUCTIONS
from bot.core.command_center import handle_message_input


async def _send_service_alert(bot: commands.Bot, channel: discord.TextChannel, alert_type: str, message: str) -> None:
    """
    Send an alert message via webhook and forward it to the agent.

    Args:
        bot (commands.Bot): The Discord bot instance.
        channel (discord.TextChannel): The channel to send messages to.
        alert_type (str): type of alert e.g. service_down
        message (str): text to send in alert

    """
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Alert Webhook")
    if webhook is None:
        webhook = await channel.create_webhook(name="Alert Webhook")

    instruction = AGENT_INSTRUCTIONS[alert_type]
    content = f"<@{bot.user.id}> {instruction} Here are the details:\n" f"{message}"
    alert_embed = discord.Embed(title="Alert", description=content, color=discord.Color.yellow())

    msg = await webhook.send(
        username="🚨 Alert",
        avatar_url="http://cdn-icons-png.flaticon.com/512/5585/5585025.png",
        embed=alert_embed,
        wait=True,
    )
    await handle_message_input(bot, msg, is_alert=True)


async def handle_webhook_input(bot: commands.Bot, channel: discord.TextChannel, data: dict):
    """
    Entry point for webhook sent to the command center.

    Args:
        bot (commands.Bot): The Discord bot instance.
        channel (discord.TextChannel): The channel to send messages to.
        data (dict): The webhook data.

    """
    alert_type = data.get("type", "").lower()
    if alert_type in AGENT_INSTRUCTIONS:
        await _send_service_alert(bot, channel, alert_type, data.get("message", ""))
    else:
        message = data.get("message", "No message provided.")
        await channel.send(f"Webhook event received: {message}")
