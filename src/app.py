# File: app.py
"""
This file contains all application logic
"""

import logging
from src.sequence import Sequence
from src.elements import Element
from src.power_state import PowerState
from src.state import State
from src.file_path import *
import json
import os

class App:
    def __init__(self):
        self.loaded_elts = self.__load_elements()
        self.dict_elts = {elt.name: elt for elt in self.loaded_elts}
        self.loaded_seqs = self.__load_sequences()
        self.dict_seqs = {seq.name: seq for seq in self.loaded_seqs}
        self.current_sequence = self.loaded_seqs[0] if len(self.loaded_seqs) > 0 else None

    def __load_elements(file_path: str = elements_path):
        """
        Load elements from a file
        """
        loaded_elts = []
        for filename in os.listdir(elements_path):
            if filename.endswith(".json"):
                with open(elements_path + filename, "r") as file:
                    logging.debug(f"Loading element from {filename}")
                    element = Element.from_dict(json.loads(file))
                    loaded_elts.append(element)
        if len(loaded_elts) == 0:
            logging.info("No element to load")
        return loaded_elts

    def __load_sequences(file_path: str = sequences_path):
        """
        Load sequences from a file
        """
        loaded_seqs = []
        for filename in os.listdir(sequences_path):
            if filename.endswith(".json"):
                with open(sequences_path + filename, "r") as file:
                    logging.debug(f"Loading sequence from {filename}")
                    sequence = Sequence.from_dict(json.loads(file))
                    loaded_seqs.append(sequence)
        if len(loaded_seqs) == 0:
            logging.info("No sequence to load")
        return loaded_seqs
    
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

    def get_element(self, index: int = -1):
        if index >= len(self.loaded_elts):
            raise IndexError("Index out of range")
        return self.loaded_elts[index]

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
    
    def remove_sequence(self, sequence: Sequence):
        """
        Remove a sequence
        """
        del self.dict_seqs[sequence.name]
        self.loaded_seqs.remove(sequence)

    def remove_state(self, sequence: Sequence, state: State):
        """
        Remove a state from a sequence
        """
        sequence.remove_state(state)

    def add_state(self, sequence: Sequence, state: State):
        """
        Add a state to a sequence
        """
        sequence.add_state(state)
    
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
    
    def set_current_sequence(self, sequence_name: str):
        """
        Set the current sequence
        """
        self.current_sequence = self.dict_seqs[sequence_name]
        logging.info(f"Current sequence set to {sequence_name}")

    def remove_element(self, element: Element):
        """
        Remove an element
        """
        del self.dict_elts[element.name]
        self.loaded_elts.remove(element)