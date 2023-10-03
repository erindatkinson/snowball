#!/usr/bin/env python
"""main entrypoint for the bot"""

import sys
from logging import error
from fire import Fire
from packages.config.config import init
from packages.services.services import clients
from packages.errors.errors import ConfigError

def Run() -> None:
    """Snowball is a bot for rolling a ball up the hill, if that ball was a number and
    rolling was posting increasing counting messages in a discord channel"""
    try:
        configs = init()
    except ConfigError as cerr:
        error(cerr)
        sys.exit(1)
    clients["discord"](configs)

if __name__ == "__main__":
    Fire(Run)
