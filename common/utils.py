import logging

def log(msg):
    logger = logging.getLogger(__name__)
    logger.exception(msg)
    logger.error(str(msg))