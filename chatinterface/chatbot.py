"""Agent definitions for the chatbot application."""

from agents import Agent


def build_agent(instructions: str):
    """Builds and returns a simple chatbot agent."""
    return Agent(
        name="Chatbot",
        instructions=instructions,
    )
