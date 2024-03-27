# File: elements.py
"""
This file contains class to represent a physical element with its power states
for example a accelerometer, a gyroscope, a sensor, a processor, etc.

names must be unique

"""

from src.power_state import *
import json

class Element:
    def __init__(self,
        name=None,
        wake:tuple[float, float] = (0, 0),
        active:tuple[float, float] = (0, 0),
        fall:tuple[float, float] = (0, 0),
        sleep:tuple[float, float] = (0, 0),
        description:str = ""
    ):

        self.name = name
        self.description = description
        self.WakeState = PowerState(wake[0], wake[1])
        self.ActiveState = PowerState(active[0], active[1])
        self.FallState = PowerState(fall[0], fall[1])
        self.SleepState = PowerState(sleep[0], sleep[1])
        
    def __str__(self):
        string = (
            f"{self.name}"
            f"{self.description}"
            f"{self.WakeState}"
            f"{self.ActiveState}"
            f"{self.FallState}"
            f"{self.SleepState}"
        )
        return string
    
    # Getters
    #===========================================================================
    def get_time(self, power_state: str):
        match power_state:
            case "Wake":
                return self.WakeState.get_time()
            case "Active":
                return self.ActiveState.get_time()
            case "Fall":
                return self.FallState.get_time()
            case "Sleep":
                return self.SleepState.get_time()
            case _:
                raise ValueError("Invalid power_state")

    def get_power(self, power_state: str):
        match power_state:
            case "Wake":
                return self.WakeState.get_power()
            case "Active":
                return self.ActiveState.get_power()
            case "Fall":
                return self.FallState.get_power()
            case "Sleep":
                return self.SleepState.get_power()
            case _:
                raise ValueError("Invalid power_state")
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def str_power_state(self, power_state: str):
        match power_state:
            case "Wake":
                return str(self.WakeState)
            case "Active":
                return str(self.ActiveState)
            case "Fall":
                return str(self.FallState)
            case "Sleep":
                return str(self.SleepState)
            case _:
                raise ValueError("Invalid power_state")
    
    def get_power_state(self, power_state: str):
        match power_state:
            case "Wake":
                return self.WakeState
            case "Active":
                return self.ActiveState
            case "Fall":
                return self.FallState
            case "Sleep":
                return self.SleepState
            case _:
                raise ValueError("Invalid power_state")

    # Setters
    #===========================================================================
    def set_description(self, description:str):
        self.description = str(description)

    def set_name(self, name:str):
        self.name = str(name)

    def edit_power_state(self,
        power_state: str,
        power: float = 0,
        time: float = 0
        ):

        match power_state:
            case "Wake":
                self.WakeState.set_power(power)
                self.WakeState.set_time(time)
            case "Active":
                self.ActiveState.set_power(power)
                self.ActiveState.set_time(time)
            case "Fall":
                self.FallState.set_power(power)
                self.FallState.set_time(time)
            case "Sleep":
                self.SleepState.set_power(power)
                self.SleepState.set_time(time)
            case _:
                raise ValueError("Invalid power_state")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "WakeState": self.WakeState.to_dict(),
            "ActiveState": self.ActiveState.to_dict(),
            "FallState": self.FallState.to_dict(),
            "SleepState": self.SleepState.to_dict()
        }

    # # Save and load
    #===========================================================================
    def __from_dict(self, dict_element: dict):
        self.name = dict_element["name"]
        self.description = dict_element["description"]
        self.WakeState = PowerState.from_dict(dict_element["WakeState"])
        self.ActiveState = PowerState.from_dict(dict_element["ActiveState"])
        self.FallState = PowerState.from_dict(dict_element["FallState"])
        self.SleepState = PowerState.from_dict(dict_element["SleepState"])
    
    def to_json(self, path: str):
        file_path = f"{path}/{self.name}.json"
        with open(file_path, "w") as file:
            file.write(json.dumps(self.to_dict(), indent=4))
            
    def from_dict(self, dict_element: dict):
        element = Element()
        element.__from_dict(dict_element)
        return element


# Function
#===========================================================================
def from_json(path: str):
    with open(path, "r") as file:
        dict_element = json.load(file)
        return Element.from_dict(dict_element)

# Dummy element
#===========================================================================
class DummyElement(Element):
    def __init__(self, name: str):
        super().__init__(
            name=f"DummyElement_{name}",
            wake=(0, 0),
            active=(0, 0),
            fall=(0, 0),
            sleep=(0, 0),
            description="This is a dummy element"
        )
