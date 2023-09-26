#!/usr/bin/env python
from fire import Fire
from packages.config.config import init


def Run(config:str=".snowball.conf") -> None:
    init(config)

if __name__ == "__main__":
    Fire(Run)
