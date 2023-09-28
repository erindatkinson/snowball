"""module to handle the ingress of configuration and setup of the logger"""
from configparser import ConfigParser
from logging import info
from packages.errors.errors import ConfigError
from .logging import init_logs

services:dict[str, dict[str, str]] = {}
core:dict[str, str]={}

def init(config:str)->(None|Exception):
    """initializes the configuration for the bot"""
    parser = ConfigParser()

    with open(config, encoding='utf-8') as fp_in:
        parser.read_file(fp_in)

    core["name"] = parser.get("core", "name", fallback="snowball")
    core["db_file"] = parser.get("core", "db_file", fallback="data/snowball.db")
    core["log_level"] = parser.get("core", "log_level", fallback="WARN").upper()

    init_logs(core["name"], core["log_level"])

    info("configuring services")
    has_service = False
    if "discord" in parser.sections():
        services["discord"] = dict(parser["discord"])
        info("discord service configured")
        has_service = True

    # adding for future integration
    if "slack" in parser.sections():
        services["slack"] = dict(parser["slack"])
        info("slack service configured")
        has_service = True

    if not has_service:
        raise ConfigError("no service defined, please add a service to your config")

