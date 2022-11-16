"""
Tests on chatbot public interface
"""
import unittest
from unittest.mock import MagicMock

import chatbot


class Message(unittest.TestCase):
    """Testcase on Message"""

    def test(self):
        """there must be a Message class in chatbot"""
        self.assertTrue(chatbot.Message)


class Interface(unittest.TestCase):
    """Testcase on entry Testcase"""

    def test(self):
        """standard interface call should work"""
        callback = MagicMock()
        conf = {"extensions": ["tests._example"], "tests._example": {"path": True}}
        bot = chatbot.Chat("unique_talker_id", callback, conf=conf)
        callback.assert_not_called()
        bot.greet()
        callback.assert_called()
        bot.ask(chatbot.Message("Hello"))
        bot.ask(chatbot.Message("example"))
        bot.close() # Important to call this, to close any resources opened related to memory
