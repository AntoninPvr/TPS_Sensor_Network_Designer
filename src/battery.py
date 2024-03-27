# File: battery.py
"""
This file contains the GUI class
"""

import logging
import json
from src.file_path import *

class Battery():
    def __init__(self,
                 name=None,
                 capacity: float=0, # in Joules
                 input_power: float=0, # in Watts
                 max_output_power: float=0, # in Watts
                 efficiency: float=1.0, 
                 current_capacity: float=0.0 # in Joules
                 ):
        
        self.name = name
        self.capacity = capacity
        self.input_power = input_power
        self.max_output_power = max_output_power
        self.efficiency = efficiency
        self.current_capacity = current_capacity

    # Getters
    #================================
    def get_name(self):
        return self.name

    def get_capacity(self):
        return self.capacity
    
    def get_input_power(self):
        return self.input_power
    
    def get_max_output_power(self):
        return self.max_output_power
    
    def get_efficiency(self):
        return self.efficiency
    
    def get_current_capacity(self):
        return self.current_capacity
    
    # Setters
    #================================
    def set_name(self, name: str):
        self.name = name
    
    def set_capacity(self, capacity: float):
        self.capacity = capacity

    def set_input_power(self, input_power: float):
        self.input_power = input_power

    def set_max_output_power(self, max_output_power: float):
        self.max_output_power = max_output_power
    
    def set_efficiency(self, efficiency: float):
        self.efficiency = efficiency
    
    def set_current_capacity(self, current_capacity: float):
        self.current_capacity = current_capacity
    
    # Save and Load
    #================================
    def to_dict(self):
        return {
            "name": self.name,
            "capacity": self.capacity,
            "input_power": self.input_power,
            "max_output_power": self.max_output_power,
            "efficiency": self.efficiency,
            "current_capacity": self.current_capacity
        }
    
    def __from_dict(self, dict: dict):
        self.name = dict["name"]
        self.capacity = dict["capacity"]
        self.input_power = dict["input_power"]
        self.max_output_power = dict["max_output_power"]
        self.efficiency = dict["efficiency"]
        self.current_capacity = dict["current_capacity"]

    def from_dict(self, dict: dict):
        battery = Battery()
        battery.__from_dict(dict)
        return battery

    def to_json(self, file_path: str=battery_file):
        with open(file_path, "w") as file:
            json.dump(self.to_dict(), file)

    # Methods
    #================================
    def discharge(self, power: float=None, time: float=None):
        if power is None:
            raise ValueError("Power must be specified")
        if time is None:
            raise ValueError("Time must be specified")
        energy = power * time
        if energy > self.current_capacity:
            logging.info("Battery is fully depleted")
            capacity = self.current_capacity
            self.current_capacity = 0
            return(capacity/power) #Return time when battery is depleted
        else:
            self.current_capacity -= energy
            logging.info(f"Battery discharged by {energy} J")
            return(None)
