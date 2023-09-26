#!/usr/bin/env python
from fire import Fire
from packages.config.config import init

def Run(config:str=".snowball.conf") -> None:
    """Snowball is a bot for rolling a ball up the hill, if that ball was a number and
    rolling was posting increasing counting messages in a discord channel"""
    init(config)

if __name__ == "__main__":
    Fire(Run)
