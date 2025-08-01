"""
WebServer module for handling incoming webhook events via HTTP POST requests using aiohttp.

This module defines a WebServer class that can start an aiohttp server,
receive JSON-formatted webhook events, and dispatch them to a bot instance.
"""

import os

from aiohttp import web

from bot.config.alerts import alerts_config
from bot.utils.console_logger import console_logger


class WebServer:
    """
    A simple asynchronous web server for receiving webhook events.

    Attributes:
        bot: An object that must have a `dispatch` method to handle webhook events.
        app: The aiohttp web application instance.

    """

    def __init__(self, bot):
        """
        Initialize the WebServer with a bot instance and sets up the HTTP route.

        Args:
            bot: The bot instance responsible for handling webhook events.

        """
        self.bot = bot
        self.app = web.Application()
        # todo: maybe move api version into a separate file or abstract urls to a constant file
        self.app.add_routes([web.post("/api/v1/webhooks/service", self.handle_request)])

    async def handle_request(self, request):
        """
        Handle incoming POST requests by parsing JSON data and dispatching it.

        Args:
            request (aiohttp.web.Request): The incoming HTTP request.

        Returns:
            aiohttp.web.Response: A simple HTTP response confirming receipt.

        """
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            console_logger.info("An unauthorized webhook request was made.")
            return web.Response(text="Unauthorized", status=401)

        token = auth_header.split("Bearer ")[1].strip()
        expected_token = alerts_config.webhook_alerts_token

        if token != expected_token:
            console_logger.info("An unauthorized webhook request was made.")
            return web.Response(text="Unauthorized", status=401)

        data = await request.json()
        self.bot.dispatch("webhook_alert_event", data)
        return web.Response(text="Event received")

    async def start(self):
        """
        Start the aiohttp web server on the specified port (default: 8180).
        """
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", os.getenv("SERVER_PORT", 8180))
        await site.start()

    async def stop(self):
        """
        Stop the web server and performs cleanup.

        Note:
            This method currently references an undefined `self.runner`.
            You may need to assign `runner` to `self.runner` in `start()` to enable cleanup.

        """
        await self.runner.cleanup()
