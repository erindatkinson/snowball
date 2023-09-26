"""module to handle the ingress of configuration and setup of the logger"""
from configparser import ConfigParser
import logging
from packages.errors.errors import ConfigError

services = {}

def init(config:str)->(None|Exception):
    """initializes the configuration for the bot"""
    parser = ConfigParser()

    with open(config, encoding='utf-8') as fp_in:
        parser.read_file(fp_in)

    name = parser.get("core", "name", fallback="snowball")
    level = parser.get("core", "log_level", fallback="WARN").upper()
    logging.basicConfig(
        level=logging.getLevelNamesMapping()[level],
        format=f"{name} [%(levelname)s] - %(message)s")

    logging.info("configuring services")
    has_service = False
    if "discord" in parser.sections():
        services["discord"] = parser["discord"]
        logging.info("discord service configured")
        has_service = True

    # adding for future integration
    if "slack" in parser.sections():
        services["slack"] = parser["slack"]
        logging.info("slack service configured")
        has_service = True

    if not has_service:
        raise ConfigError("no service defined, please add a service to your config")
