"""module to handle the ingress of configuration and setup of the logger"""

from packages.expectenv.expectenv import ExpectEnvParser
from .logging import init_logs

class Configs:
    """class to manage the various configs for the app"""
    def __init__(self, configs):
        self.configs = configs
    
    def must_get(self, key, namespace=None)->str:
        """get but it raises key error if not found"""
        if namespace is None:
            return self.configs["core"][key]
        else:
            return self.configs[namespace][key]

    def get(self, key, namespace=None)->str|None:
        """get pulls a key from a namespace or None if not found"""
        if namespace is None:
            core_keys = self.configs.get("core")
            if core_keys is None:
                return None
            else:
                return core_keys.get(key)
        ns_keys = self.configs.get(namespace)
        if ns_keys is None:
            return None
        else:
            return ns_keys.get(key)

def init()->(Configs|Exception):
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
    data = parser.parse()
    configs = Configs(data)
    init_logs(configs.must_get("name"), configs.must_get("log_level"))
    return configs
