"""module to handle the ingress of configuration and setup of the logger"""

from packages.expectenv.expectenv import ExpectEnvParser
from .logging import init_logs


class Configs:
    """class to manage the various configs for the app"""

    def __init__(self, configs):
        self.configs = configs

    def get(self, key, namespace=None) -> str:
        """get pulls a key from a namespace or raises a KeyError if not found"""
        if namespace is None:
            return self.configs["core"][key]
        return self.configs[namespace][key]


def init() -> Configs | Exception:
    """initializes the configuration for the bot"""
    parser = ExpectEnvParser("bot")
    parser.bind("name")
    parser.bind("database")
    parser.bind("log_level")
    parser.bind("admin_guild", "discord")
    parser.bind("admin_role", "discord")
    parser.bind("channel", "discord")
    parser.bind("app_key", "discord")
    parser.bind("public_key", "discord")
    parser.bind("token", "discord")
    parser.bind("reset_emoji", "discord")
    parser.bind("mutex_hold", "discord")
    data = parser.parse()
    configs = Configs(data)
    init_logs(configs.get("name"), configs.get("log_level"))
    return configs
