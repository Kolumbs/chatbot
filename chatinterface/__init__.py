"""Runs simple chatbot."""

import os

import membank

os.environ["OPENAI_DEFAULT_MODEL"] = "gpt-5-nano"


__all__ = ["membank"]
