from json import load
from logging.config import dictConfig
from os import path

LOGGER_PATH = path.join(path.dirname(__file__), "loggers.json")

with open(LOGGER_PATH) as loggers:
    dictConfig(load(loggers))
