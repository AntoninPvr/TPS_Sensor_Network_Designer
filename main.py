# File: main.py
"""
This file contains the main entry point for the program
"""

#from gui import GUI
import logging
from src.arguments import parse_arguments
from src.app import App
from src.command_line import CommandLine
import src.gui.gui as gui
from test import test_app

def init_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting the program...")

if __name__ == "__main__":
    args = parse_arguments()
    if args.DEBUG:
        logging.info("Running the program in debug mode")
        init_logging("DEBUG")
        app = test_app()
    else:
        logging.info("Running the program in normal mode")
        init_logging(args.log_level)
        app = App()

    if args.no_gui:
        logging.info("Running the program without GUI")
        app_cmd = CommandLine(app)
    else:
        logging.info("Running the program with GUI")
        app_gui = gui.GUI(app)
        app_gui.mainloop()