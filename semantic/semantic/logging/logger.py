import os
import logging.config
from .log_config import LOGGING_CONFIG


def logger_setup():
    """Sets up logger configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)


logger = logging.getLogger(os.getenv("LOG_NAME"))
