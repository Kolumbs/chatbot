"""Agent definitions for the chatbot application."""

from dataclasses import dataclass

import membank
from agents import Agent
from zoozl.chatbot import MessagePart, Package


def build_agent(instructions: str):
    """Builds and returns a simple chatbot agent."""
    return Agent(
        name="Chatbot",
        instructions=instructions,
    )


@dataclass
class Context:
    """Context for chatbot."""

    conf: dict
    memory: membank.LoadMemory
    package: Package
    message_parts: list[MessagePart]
