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

    def setUp(self):
        self.callback = MagicMock()

    def assert_called_with(self, *args):
        """check for mock call"""
        for arg in args:
            self.callback.assert_called_with(chatbot.Message(arg))

    def test(self):
        """standard interface call should work"""
        conf = {"extensions": ["tests._example"], "tests._example": {"path": True}}
        bot = chatbot.Chat("unique_talker_id", self.callback, conf=conf)
        self.callback.assert_not_called()
        bot.greet()
        self.callback.assert_called()
        self.callback.reset_mock()
        bot.ask(chatbot.Message("example"))
        self.assert_called_with("example")
        self.callback.reset_mock()
        bot.ask(chatbot.Message("help"))
        bot.close() # Important to call this, to close any resources opened related to memory
