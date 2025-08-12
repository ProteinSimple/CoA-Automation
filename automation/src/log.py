import logging


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)
