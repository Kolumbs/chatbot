"""Command line utility to start simple chatbot."""

import argparse
import sys

import tomllib
from zoozl.server import start

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chatbot",
        description="Start chatbot server to listen to different inputs.",
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Path to toml configuration file.",
    )
    args = parser.parse_args()
    with open(args.config_path, "rb") as f:
        config = tomllib.load(f)
    if "chatbot" not in config:
        print("No `chatbot` configuration found in config file.")
        sys.exit(1)
    chatbot_cfg = config["chatbot"]
    if "database" not in chatbot_cfg:
        print(
            "No `database` configuration found in `chatbot` section of config."
        )
        sys.exit(1)
    zoozl_cfg = {
        "memory_path": f'sqlite://{config["chatbot"]["database"]}',
        "extensions": ["chatinterface.plugin"],
        "chatbot": chatbot_cfg,
    }
    if "log_level" in chatbot_cfg:
        zoozl_cfg["log_level"] = chatbot_cfg["log_level"]
    if "auth_required" in chatbot_cfg:
        zoozl_cfg["auth_required"] = chatbot_cfg["auth_required"]
    if "websocket" in chatbot_cfg:
        if "port" in chatbot_cfg["websocket"]:
            zoozl_cfg["websocket_port"] = chatbot_cfg["websocket"]["port"]
        else:
            print(
                "No websocket port specified in config. Using default 8080."
            )
            zoozl_cfg["websocket_port"] = 8080
    start(zoozl_cfg)
