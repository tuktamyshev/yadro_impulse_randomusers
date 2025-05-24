import logging
import logging.config
import os

from config import BASE_DIR

LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
        },
        "filters": {
            "webserver": {"()": "logging.Filter", "name": "webserver"},
            "user": {"()": "logging.Filter", "name": "user"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "webserver": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/webserver.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "DEBUG",
                "filters": ["webserver"],
            },
            "user": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/user.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "DEBUG",
                "filters": ["user"],
            },
        },
        "loggers": {
            "webserver": {
                "level": "DEBUG",
                "handlers": ["webserver", "console"],
            },
            "user": {
                "level": "DEBUG",
                "handlers": ["user", "console"],
            },
        },
    }

    logging.config.dictConfig(logging_config)
