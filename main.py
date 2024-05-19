# File: main.py
"""
This file contains the main entry point for the program
"""

#from gui import GUI
from src.arguments import parse_arguments
from src.app import App
from src.command_line import CommandLine
import src.gui.gui as gui
from test import test_app
from src.logger import *

if __name__ == "__main__":
    args = parse_arguments()
    if args.DEBUG:
        logger.info("Running the program in debug mode")
        init_logger(logger, "DEBUG")
        app = test_app()
    else:
        logger.info("Running the program in normal mode")
        init_logger(logger, args.log_level)
        app = App()

    if args.no_gui:
        logger.info("Running the program without GUI")
        app_cmd = CommandLine(app)
    else:
        logger.info("Running the program with GUI")
        app_gui = gui.GUI(app)
        app_gui.mainloop()