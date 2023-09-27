"""main entrypoint for the bot"""

#!/usr/bin/env python
import sys
from logging import error
from multiprocessing import Pool
from fire import Fire
from packages.config.config import init, services
from packages.services.services import clients
from packages.errors.errors import ConfigError

def Run(config:str=".snowball.conf") -> None:
    """Snowball is a bot for rolling a ball up the hill, if that ball was a number and
    rolling was posting increasing counting messages in a discord channel"""
    try:
        init(config)
        with Pool(2) as pool:
            pool.apply_async(lambda service: clients[service](), services.keys())
    except ConfigError as cerr:
        error(cerr)
        sys.exit(1)


if __name__ == "__main__":
    Fire(Run)
