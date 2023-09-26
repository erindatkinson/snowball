from configparser import ConfigParser
from sys import exit
import logging


def init(config)->(dict|Exception):
   parser = ConfigParser()
   with open(config) as fp_in:
    parser.readfp(fp_in)

    name = parser.get("core", "name", fallback="snowball")
    level = parser.get("core", "log_level", fallback="WARN").upper()
    logging.basicConfig(level=logging.getLevelNamesMapping()[level])






    
   
