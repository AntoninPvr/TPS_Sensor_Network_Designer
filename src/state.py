from src.elements import Element, DummyElement
import json
import logging

"""
State class, that store set of elements and their power state

name must be unique

"""

class State:
    def __init__(self,
                name=None,
                description: str = "",
                elements=[] #[{"element": None, "power_state": None}]
                ):
        
        self.elements = elements
        self.name = str(name)
        self.description = str(description)
    
    def __str__(self):
        string = (
            f"{self.name}"
            f"{self.description}"
            f"{self.elements}"
        )
        return string
    
    # Getters
    #===========================================================================
    def get_element(self, index: int = -1):
        """
        Returns the element at index
        by default, return the last element
        """
        return self.elements[index]
    
    def get_energy(self):
        """
        Returns the energy consumption of the state
        """
        for elt in self.elements:
            energy = 0
            energy += elt["element"].get_power(elt["power_state"]) * elt["element"].get_time(elt["power_state"])
        return energy
    
    def get_max_power(self):
        """
        Returns the maximum power consumption of the state
        Max power is at the beginning of the state
        """
        max_power = 0
        for elt in self.elements:
            max_power += elt["element"].get_power(elt["power_state"])
        return max_power
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description

    # Setters
    #===========================================================================
    def set_description(self, description: str = ""):
        self.description = str(description)
        logging.info(f"{self.name}'s description is: {description}")
    
    def set_name(self, name: str):
        self.name = name
        logging.info(f"State name set to {name}")

    # Methods
    #===========================================================================
    def add_element(self, element=[{"element": None, "power_state": None}]):
        self.elements.append(element)

    def generate_power_data(self):
        """
        Returns the power consumption of the state
        All device boot at the same time, and state end when the last device change state
        
        Example: with 3 devices A, B and C
        __
          |            
          |____
               |_____   
        |A|
        |  B   |
        |      C     |	
        """
        X = []
        T = []
        sorted_elements = sorted(self.elements, key=lambda x: x["element"].get_time(x["power_state"]))
        for i in range(len(sorted_elements)):
            X.append(0)
            for j in range(len(sorted_elements)-i):
                X[i] += sorted_elements[j]["element"].get_power(sorted_elements[j]["power_state"])
            T.append(sorted_elements[i]["element"].get_time(sorted_elements[i]["power_state"]))
        return X, T

    # Save and load
    #===========================================================================
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "list_elements": [{"element": elt["element"].get_name(), "power_state": elt["power_state"]} for elt in self.elements]
        }
    def from_dict(dict_state, dict_elements: dict, dict_available_elts: dict):
        state = State()
        state.name = dict_state["name"]
        state.description = dict_state["description"]
        list_elements = dict_state["list_elements"]
        for elt_name in list_elements:
            try:
                new_element = dict_available_elts[elt_name]
            except KeyError:
                new_element = DummyElement(elt_name)
                logging.error(f"Element {elt_name} not found, replaced by a dummy element")
            state.elements.append({"element": new_element, "power_state": elt_name["power_state"]})
    
    def to_json(self, file_path: str):
        with open(file_path, "w") as file:
            json.dump(self.to_dict(), file)