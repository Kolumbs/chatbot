"""Assistant plugin to zoozl server.

Plugin allows for zoozl server library to handle incoming messages.
"""

import datetime

from agents import (
    set_default_openai_key,
    Runner,
    SQLiteSession,
    RunContextWrapper,
    RunConfig,
    TResponseInputItem,
)
from zoozl.chatbot import (
    Interface,
    Package,
    InterfaceRoot,
    Message,
    MessagePart,
)

from . import chatbot
import logging

log = logging.getLogger(__name__)


class Session(SQLiteSession):
    """Session that limits message history."""

    window_size = 10

    def __init__(self, session_id, db_path):
        super().__init__(session_id=session_id, db_path=db_path)

    async def get_items(self, limit: int | None = None):
        """Override to only return the last N messages."""
        if limit is None:
            limit = self.window_size
        items = await super().get_items(limit=limit)
        while limit is not None and items:
            if items[0].get("role") == "user":
                break
            items.pop(0)
        return items


class Chatbot(Interface):
    """Chatbot interface to zoozl."""

    aliases = {"chatbot", "help", "greet"}

    def load(self, root: InterfaceRoot):
        """Load OpenAI agents."""
        try:
            api_key = root.conf["chatbot"]["openai_api_key"]
            set_default_openai_key(api_key)
        except KeyError:
            raise RuntimeError(
                "Chatbot requires openAI api key to work!"
            ) from None
        self.agent = chatbot.build_agent(root.conf["chatbot"]["prompt"])
        self.conf = root.conf
        self.db_path = self.conf["chatbot"]["database"]
        self.memory = root.memory

    async def consume(self, package: Package):
        """Handle incoming message."""
        context = RunContextWrapper(
            chatbot.Context(
                conf=self.conf["chatbot"],
                memory=self.memory,
                package=package,
                message_parts=[],
            )
        )
        run = await Runner.run(
            self.agent,
            [
                {"role": "user", "content": package.last_message.text},
                {
                    "role": "system",
                    "content": f"Time: {datetime.datetime.now().isoformat()}\n"
                },
            ],
            run_config=RunConfig(session_input_callback=input_callable),
            session=Session(package.talker, self.db_path),
            context=context.context,
        )
        msg = Message(author="agent")
        if context.context.message_parts:
            for f in context.context.message_parts:
                msg.parts.append(f)
        msg.parts.append(MessagePart(text=run.final_output))
        package.callback(msg)


def input_callable(
    history: list[TResponseInputItem], new: list[TResponseInputItem]
) -> list[TResponseInputItem]:
    """Input callable to pass context."""
    return history + new
