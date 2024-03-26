# File: commande_line.py
"""
This file contains the command line interface
"""

import logging
from src.app import App

class CommandLine:
    def __init__(self, app: App = App()):
        self.app = app

        logging.info("Running the program without GUI")
        logging.warning("The command line interface is not implemented yet")
        raise NotImplementedError("The command line interface is not implemented yet")