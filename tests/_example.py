"""This is example module to load as extension"""
from chatbot import Interface


class Sample(Interface):
    """Sample test extension"""
    aliases = {"example"}

    def consume(self, package):
        if "path" not in self.conf:
            raise RuntimeError("Path must be configured")
        package.callback("example")
