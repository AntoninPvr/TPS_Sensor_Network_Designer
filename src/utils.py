# File: utils.py
"""
This file contains utility functions
"""
import re
from src.logger import logger

def s2f(string: str) -> float:
    """
    Convert a string to a float
    """
    if string == "":
        return 0
    else:
        pattern = r'(\d*\.?\d*)([a-zA-Z]*)'
        match = re.match(pattern, string)
        unit = match.group(2)
        if unit == '':
            return float(string)
        else:
            units= {
                'f': 1e-15, # femto
                'p': 1e-12, # pico
                'n': 1e-9, # nano
                'u': 1e-6, # micro
                'm': 1e-3, # milli
                'k': 1e3, # kilo
                'M': 1e6, # mega
                'G': 1e9, # giga
                'T': 1e12, # tera
                'P': 1e15, # peta
            }
            value = float(match.group(1))
            if unit in units:
                return value*units[unit]
            else:
                raise ValueError("Invalid unit")

def f2s(value: float, ndigit: int=4) -> str:
    """
    Convert a float to a string
    """
    if value == 0:
        return "0"
    else:
        units= {
            'f': 1e-15, # femto
            'p': 1e-12, # pico
            'n': 1e-9, # nano
            'u': 1e-6, # micro
            'm': 1e-3, # milli
            '': 1, # unit
            'k': 1e3, # kilo
            'M': 1e6, # mega
            'G': 1e9, # giga
            'T': 1e12, # tera
            'P': 1e15, # peta
        }
        last_unit = 'f'
        for unit in units:
            if value < units[unit]:
                return f"{round(value/units[last_unit], ndigit)}{last_unit}"
            last_unit = unit

def cheat_data_for_graph(T, Y):
    """
    Cheat data for graph
    adding fake time and power value to fix the graph
    """
    logger.debug(f"Y: {Y}")
    logger.debug(f"T: {T}")
    newT = [T[0]]
    newY = [Y[0]]
    for i in range(1, len(T)):
        newT.append(T[i]-(T[i]-T[i-1])/100)
        newY.append(Y[i-1])
        newT.append(T[i])
        newY.append(Y[i])
    logger.debug("===")
    logger.debug(f"Y: {newY}")
    logger.debug(f"T: {newT}")
    return newT, newY
