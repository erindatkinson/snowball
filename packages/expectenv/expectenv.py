"""a package to kinda hack together something
similar to how golang viper works for pulling
environment variables"""
from os import getenv

class EnvError(Exception):
    """error for missing env"""

class ExpectEnvParser:
    """ExpectEnvParser is a parser class to manage expected environment variables
    and pulling them in from the system"""
    def __init__(self, prefix:str|None=None):
        self.prefix = prefix
        self.keys:list[str] = []
        self.sections = {}

    def bind(self, key:str, section:str|None=None):
        """bind sets that a key is expected to be in the environment for the application
        if a prefix was set, it expects it under {prefix}_{key}, if a section is set,
        it expects it under ({prefix}_){section}_{key} with optional prefix"""
        if section is None:
            self.keys.append(key)
        else:
            try:
                self.sections[section].append(key)
            except KeyError:
                self.sections[section] = [key]

    def parse(self)->dict:
        """parse looks through all the bound expectations and attempts to pull them
        into a dict, if it cannot find one, it raises an EnvError, keys not bound to a
        section are put in the 'core' section"""
        core_out = {}
        section_out = {}
        for key in self.keys:
            if self.prefix is not None:
                envkey = key.upper()
            envkey = f"{self.prefix}_{key}".upper()
            val = getenv(envkey)
            if val is None:
                raise EnvError(f"missing env var: {envkey}")
            core_out[key] = val
        for section, section_keys in self.sections.items():
            for key in section_keys:
                envkey = f"{self.prefix}_{section}_{key}".upper()
                val = getenv(envkey)
                if val is None:
                    raise EnvError(f"missing env var: {envkey}")
                try:
                    section_out[section][key] = val
                except KeyError:
                    section_out[section] = {
                        key: val
                    }
        out = {
            "core": core_out
        }
        out.update(section_out)
        
        return out
