"""module to manage logging"""
from logging import Formatter, StreamHandler, FileHandler, getLevelNamesMapping, basicConfig
from typing import Any
from sys import stdout

log:dict[str, Any] = {}

def init_logs(name:str, level:str)->None:
    """initialize the default logger and the global bits"""
    log["formatter"] = Formatter(f"{name} [%(levelname)s] - %(message)s")
    log["level"] = getLevelNamesMapping()[level]
    log["handler"] = StreamHandler(stream=stdout)
    f_handler = FileHandler(filename=f"{name}.log")
    log["handler"].setFormatter(log["formatter"])
    log["handler"].setLevel(log["level"])
    basicConfig(level=log["level"], handlers=[log["handler"], f_handler])
