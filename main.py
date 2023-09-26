#!/usr/bin/env python
from fire import Fire
from packages.config.config import init
from sys import exit
import logging

def Run(config:str=".snowball.conf") -> None:
    """Snowball is a bot for rolling a ball up the hill, if that ball was a number and
    rolling was posting increasing counting messages in a discord channel"""
    try:
        init(config)
    except Exception as e:
        logging.error(e)
        exit(1)


if __name__ == "__main__":
    Fire(Run)
