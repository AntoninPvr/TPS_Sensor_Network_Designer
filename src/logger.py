# File: logger.py
"""
This file contains the logger
"""
import logging

logger = logging.getLogger("SND")

def init_logger(logger=None, log_level="INFO"):
    c_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
    c_handler.setFormatter(formatter)
    logger.addHandler(c_handler)
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logger.setLevel(numeric_level)
    logger.info("Starting the program...")