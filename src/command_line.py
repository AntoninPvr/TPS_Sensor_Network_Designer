# File: commande_line.py
"""
This file contains the command line interface
"""

from src.logger import logger
from src.app import App

class CommandLine:
    def __init__(self, app: App = App()):
        self.app = app

        logger.info("Running the program without GUI")
        logger.warning("The command line interface is not implemented yet")
        raise NotImplementedError("The command line interface is not implemented yet")