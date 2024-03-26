# File: power_state.py
"""
This file contains class to represent power state of a device
"""

class PowerState:
    def __init__(self, power: float = 0, time: float = 0):
        self.power = power
        self.time = time
        
    def __str__(self):
        string = (
            f"Power {self.power} W for {self.time} s"
        )
        return string
    
    # Getters
    #===========================================================================
    def get_power(self):
        return self.power
        
    def get_time(self):
        return self.time
        
    def get_energy(self):
        return self.power*self.time
        
    # Setters
    #===========================================================================
    def set_power(self, power: float = 0):
        self.power = power
        
    def set_time(self, time: float = 0):
        self.time = time

    # Save and load
    #===========================================================================
    def to_dict(self):
        return {
            "power": self.power,
            "time": self.time
        }
    
    def __from_dict(self, dict_power_state: dict):
        self.power = dict_power_state["power"]
        self.time = dict_power_state["time"]
    
    def from_dict(dict_power_state: dict):
        power_state = PowerState()
        power_state.__from_dict(dict_power_state)
        return power_state