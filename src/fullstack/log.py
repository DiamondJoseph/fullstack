import logging

from fullstack.config import LoggingConfig


def set_up_logging(logging_config: LoggingConfig) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging_config.level)
