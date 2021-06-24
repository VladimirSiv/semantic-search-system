import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_PATH = os.getenv("LOG_PATH")
LOG_NAME = os.getenv("LOG_NAME")

LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {
            "level": "NOTSET",
            "handlers": [],
        },
        LOG_NAME: {
            "level": LOG_LEVEL,
            "handlers": [
                "console_handler",
                "file_handler",
            ],
        },
    },
    "formatters": {
        "default": {
            "format": (
                "%(asctime)s-%(levelname)s-%(name)s-%(process)d::"
                "%(module)s|%(lineno)s:: %(message)s"
            )
        },
    },
    "handlers": {
        "console_handler": {
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                LOG_PATH,
                LOG_NAME + ".log",
            ),
            "mode": "a",
        },
    },
}
