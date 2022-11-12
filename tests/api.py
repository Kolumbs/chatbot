"""
Tests on chatbot public interface
"""
import unittest

import chatbot


class Message(unittest.TestCase):
    """Testcase on Message"""

    def test(self):
        """there must be a Message class in chatbot"""
        self.assertTrue(chatbot.Message)
