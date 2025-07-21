"""
Prompt module for representing a prompt object.
"""

from dataclasses import dataclass


@dataclass
class Prompt:
    """
    Represents a prompt with a title and content.
    """

    title: str
    content: str
