"""
SmartChat service module for handling AI interaction via HTTP.

This module manages the lifecycle of an aiohttp session and defines
logic for communicating with the external SmartChat API. It includes
functions to start and close sessions and retrieve AI-generated
responses based on user input.
"""

from typing import Optional

import aiohttp

from bot.config.smart_chat import smart_chat_config


async def start_session() -> aiohttp.ClientSession:
    """
    Start and return a new aiohttp client session.

    Returns:
        aiohttp.ClientSession: A new asynchronous HTTP session.

    """
    return aiohttp.ClientSession()


async def close_session(session: aiohttp.ClientSession):
    """
    Close the provided aiohttp session.

    Args:
        session (aiohttp.ClientSession): The session to close.

    """
    await session.close()


async def get_ai_response(session: aiohttp.ClientSession, message_content: str) -> Optional[str]:
    """
    Get an AI-generated response for the given message content.

    Sends a request to the SmartChat API with the user's message and returns
    the generated response if applicable.

    Args:
        session (aiohttp.ClientSession): The active HTTP session.
        message_content (str): The content of the message to process.

    Returns:
        Optional[str]: The AI-generated response, or None if no response should be sent.

    """
    payload = {"type": "BASIC_RAG", "content": message_content}

    try:
        async with session.post(smart_chat_config.smart_chat_api_url, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("respond") and data.get("content", "").strip() != "":
                    return data["content"]
        return None
    except Exception as e:
        print(f"SmartChat API request failed: {e}")
        return None
