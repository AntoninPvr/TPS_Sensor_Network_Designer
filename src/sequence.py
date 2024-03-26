# File: sequence.py
"""
This file contains class to represent a sequence of states
"""

from src.state import State
from src.elements import Element
import json
import logging

class Sequence:
    def __init__(self,
        name=None,
        description: str = "",
        states=[],
        dict_elts=None
        ):

        self.name = str(name)
        self.description = str(description)
        self.states = states
        self.elements = None
        self.dict_elts = dict_elts
        logging.debug(f"Sequence {self.name} created")

    # Getters
    #===========================================================================
    def get_energy(self):
        """
        Returns the energy consumption of the sequence
        """
        energy = 0
        for state in self.states:
            energy += state.get_energy()
        return energy
    
    def get_max_power(self):
        """
        Returns the maximum power consumption of the sequence
        """
        return max(self.states, key=lambda x: x.get_max_power())

    def get_name(self):
        return self.name

    # Setters
    #===========================================================================
    def set_name(self, name: str):
        self.name = name
        logging.info(f"Sequence name set to {name}")
        
    def set_description(self, description: str):
        self.description = description
        logging.info(f"{self.name}'s description is: {description}")
    
    def add_state(self, state: State):
        self.states.append(state)
        logging.info(f"State {state.name} added to sequence {self.name}")
    
    def remove_state(self, state: State):
        self.states.remove(state)
        logging.info(f"State {state.name} removed from sequence {self.name}")
    
    def set_dict_elts(self, dict_elts: dict):
        self.dict_elts = dict_elts
        logging.debug(f"Dictionary of elements set for sequence {self.name}")

    # Methods
    #===========================================================================
    def generate_power_data(self):
        """
        Returns the power consumption of the sequence
        """
        X = []
        T = []
        for state in self.states:
            Xstate, Tstate = state.generate_power_data()
            X += Xstate # Concatenate power lists
            last_time = T[-1] if T else 0
            for t in Tstate:
                T.append(t+last_time)
        return X, T
    
    def shift_states(self, initial: int=0, state: State=None):
        """
        Shift all states in a sequence after initial
        """
        self.states.insert(initial, state)

    # Save and load
    #===========================================================================
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "states": [state.to_dict() for state in self.states]
        }
    
    def __from_dict(self, dict_sequence: dict):
        self.name = dict_sequence["name"]
        self.description = dict_sequence["description"]
        self.states = [State.from_dict(dict_state, self.dict_elts) for dict_state in dict_sequence["states"]]

    def from_dict(dict_sequence: dict):
        sequence = Sequence()
        sequence.__from_dict(dict_sequence)
        return sequence
    
    def to_json(self, file_path: str):
        with open(file_path, "w") as file:
            json.dump(self.to_dict(), file, indent=4)