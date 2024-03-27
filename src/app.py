# File: app.py
"""
This file contains all application logic
"""

import logging
from src.sequence import Sequence
from src.elements import Element
from src.power_state import PowerState
from src.state import State
from src.battery import Battery
from src.file_path import *
import json
import os

class App:
    def __init__(self):

        # Attributes
        #================================
        self.loaded_elts = self.__load_elements()
        self.dict_elts = {elt.name: elt for elt in self.loaded_elts}
        self.loaded_seqs = self.__load_sequences()
        self.dict_seqs = {seq.name: seq for seq in self.loaded_seqs}
        self.current_sequence = self.loaded_seqs[0] if len(self.loaded_seqs) > 0 else None
        self.battery = self.__load_battery()
        self.current_state = 0

    # Load and save functions
    #================================
    def __load_elements(self, file_path: str = elements_path):
        """
        Load elements from a file
        """
        loaded_elts = []
        for filename in os.listdir(file_path):
            if filename.endswith(".json"):
                with open(file_path + filename, "r") as file:
                    logging.debug(f"Loading element from {filename}")
                    data = file.read()
                    element = Element.from_dict(self, json.loads(data))
                    loaded_elts.append(element)
        if len(loaded_elts) == 0:
            logging.info("No element to load")
        return loaded_elts

    def __load_sequences(self, file_path: str = sequences_path):
        """
        Load sequences from a file
        """
        loaded_seqs = []
        for filename in os.listdir(file_path):
            if filename.endswith(".json"):
                with open(file_path + filename, "r") as file:
                    logging.debug(f"Loading sequence from {filename}")
                    data = file.read()
                    sequence = Sequence.from_dict(self, json.loads(data))
                    loaded_seqs.append(sequence)
        if len(loaded_seqs) == 0:
            logging.info("No sequence to load")
        return loaded_seqs
    
    def __load_battery(self, file_path: str = battery_file):
        """
        Load battery from a file
        """
        with open(file_path, "r") as file:
            logging.debug(f"Loading battery from {battery_file}")
            data = file.read()
            battery = Battery.from_dict(self, json.loads(data))
        return battery
    
    def save_elements(self, file_path: str = elements_path):
        """
        Save elements to a file
        """
        for element in self.loaded_elts:
            element.to_json(file_path)

    def save_sequences(self, file_path: str = sequences_path):
        """
        Save sequences to a file
        """
        for sequence in self.loaded_seqs:
            sequence.to_json(file_path)
    
    def save_battery(self, file_path: str = battery_file):
        """
        Save battery to a file
        """
        self.battery.to_json(file_path)

    # adding and removing functions
    #================================
    def add_element(self, element: Element):
        """
        Add an element to the list of loaded elements
        """
        self.loaded_elts.append(element)
        self.dict_elts[element.name] = element

    def add_sequence(self, sequence: Sequence):
        """
        Add a sequence to the list of loaded sequences
        """
        self.loaded_seqs.append(sequence)
        self.dict_seqs[sequence.name] = sequence

    def add_state(self, sequence: Sequence, state: State):
        """
        Add a state to a sequence
        """
        sequence.add_state(state)

    # Getters
    #================================
    def get_element(self, index: int = -1):
        if index >= len(self.loaded_elts):
            raise IndexError("Index out of range")
        return self.loaded_elts[index]

    # Setters
    #================================
    def set_current_sequence(self, sequence_name: str):
        """
        Set the current sequence
        """
        self.current_sequence = self.dict_seqs[sequence_name]
        logging.info(f"Current sequence set to {sequence_name}")

    # Creaters
    #================================
    def create_element(self):
        """
        Create a new element
        """
        return(Element())

    def create_state(self):
        """
        Create a new power state
        """
        return(State())

    def create_sequence(self):
        """
        Create a new sequence
        """
        return(Sequence())

    # Removers
    #================================
    
    def remove_sequence(self, sequence: Sequence):
        """
        Remove a sequence
        """
        del self.dict_seqs[sequence.name]
        self.loaded_seqs.remove(sequence)

    def remove_state(self, state: State, sequence: Sequence=None):
        """
        Remove a state from a sequence

        None is the current sequence
        """
        if sequence is None:
            sequence = self.current_sequence
        sequence.remove_state(state)

    def remove_element(self, element: Element):
        """
        Remove an element
        """
        del self.dict_elts[element.name]
        self.loaded_elts.remove(element)
    
    # Methods
    #================================
    def shift_state(self, sequence: Sequence, initial: int=0, state: State=None):
        """
        Shift all states in a sequence after initial
        """
        sequence.shift_state(initial, state)

    def generate_power_data(self):
        """
        Returns the power consumption of the current sequence
        """
        return self.current_sequence.generate_power_data()

    def step_state(self, n_step: int=0):
        """
        Step the current state
        """
        final_state_index = n_step
        if final_state_index < 0:
            raise IndexError("Index out of range Too low")
        if final_state_index >= len(self.current_sequence.states):
            raise IndexError("Index out of range Too high")
        
        for i in range(1, final_state_index+1):
            state_powers = self.current_sequence.states[i].get_power()
            state_times = self.current_sequence.states[i].get_time()
            for power, time in zip(state_powers, state_times):
                self.battery.discharge(power, time)
        self.current_state = final_state_index

                    
            
            
