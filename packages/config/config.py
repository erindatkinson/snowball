from configparser import ConfigParser
from sys import exit
import logging

services = {}

def init(config:str)->(None|Exception):
   """initializes the configuration for the bot"""
   parser = ConfigParser()
   with open(config) as fp_in:
    parser.readfp(fp_in)

    name = parser.get("core", "name", fallback="snowball")
    level = parser.get("core", "log_level", fallback="WARN").upper()
    logging.basicConfig(level=logging.getLevelNamesMapping()[level])
   
   hasService = False
   if "discord" in parser.sections():
     services["discord"] = parser["discord"]
     hasService = True

   # adding for future integration
   if "slack" in parser.sections():
     services["slack"] = parser["slack"]
     hasService = True

   if not hasService:
     raise Exception("no service defined, please add a discord or slack section to your config")
