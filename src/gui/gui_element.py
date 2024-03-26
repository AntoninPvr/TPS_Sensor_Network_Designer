# File: gui_element.py
"""
This file contains the GUI element classes
"""
import customtkinter
from src.app import App
from src.power_state import PowerState
from src.elements import Element
from src.sequence import Sequence
from src.state import State

import logging
from src.utils import s2f, f2s
import src.gui.base_gui as basegui

# Colors
RED = "#e64040"
DARK_RED = "#d13d3d"

# Power states colors
WAKE_COLOR = "#8deba0"
SLEEP_COLOR = "#eb8d8d"
IDLE_COLOR = "#ebe88d"
ACTIVE_COLOR = "#8dc7eb"

class ElementPannel(customtkinter.CTkFrame, basegui.BaseGUIInstance):
    def __init__(self, master, app=None, elt_list=None, **kwargs):
        if elt_list is None:
            raise ValueError("Element must be provided")
        super().__init__(master, **kwargs)
        # Attributes
        #===========================================================================
        self.app = app

        # configure windows
        #===========================================================================
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Header
        #===========================================================================
        self.header = ElementPannelHeader(self)
        self.header.grid(row=0, column=0, sticky="nsew")

        # Scrollable elements
        #===========================================================================
        self.scrollableElements = ScrollableElementPannel(self, elt_list)
        self.scrollableElements.grid(row=1, column=0, sticky="nsew")
    # Methods
    #===========================================================================
    def update_scollable_elements(self, element):
        self.scrollableElements.add_element(element)

class ElementPannelHeader(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # configure windows
        #===========================================================================
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title pannel
        #===========================================================================
        self.name = customtkinter.CTkLabel(self,
                                        text="Available elements",
                                        bg_color="gray",
                                        padx=10
                                        )
        self.name.grid(row=0, column=0)

        # Add create element button
        #===========================================================================
        self.add_button = customtkinter.CTkButton(self, text="Add element", command=self.create_element)
        self.add_button.grid(row=0, column=2, sticky="e")

    # Methods
    #===========================================================================
    def create_element(self):
        logging.debug("Creating new element")
        CreateElement(self.master)

class ScrollableElementPannel(customtkinter.CTkScrollableFrame):
    def __init__(self, master, elt_list=None, **kwargs):
        if elt_list is None:
            raise ValueError("Element must be provided")
        super().__init__(master, **kwargs)
        # Attributes
        #===========================================================================
        self.elt_list = elt_list
        self.elt_frames = []
        self.PADX = 2
        self.PADY = 2

        # configure windows
        #===========================================================================
        self.grid_columnconfigure(0, weight=0)

        # Add elements
        #===========================================================================
        for elt in elt_list:
            self.add_element(elt)

    # Methods
    #===========================================================================
    def add_element(self, element):
        elt_frame = ElementFrame(self, element=element)
        elt_frame.grid(row=len(self.elt_frames), column=0, padx=self.PADX, pady=self.PADY, sticky="nsew")
        self.elt_frames.append(elt_frame)
        
class ElementFrame(customtkinter.CTkFrame):
    def __init__(self, master, element=None, **kwargs):
        if element is None:
            raise ValueError("Element must be provided")
        super().__init__(master,  border_width=1, **kwargs)
        # Attributes
        #===========================================================================
        self.element = element
        self.master = master
        PADX = 2
        PADY = 2

        # configure windows
        #===========================================================================
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=0)

        # configure header
        #===========================================================================
        self.header = customtkinter.CTkFrame(self)
        self.header.grid(row=0, column=0, padx=10, sticky="nsew")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0)

        # Element name
        self.name = customtkinter.CTkLabel(self.header, text=element.get_name())
        self.name.grid(row=0, column=0, padx=10, sticky="w")

        # Delete button
        def delete_item():
            logging.debug(f"Deleting {element.get_name()}")
            self.destroy()
            master.elt_frames.remove(self)
        self.destroy_button = customtkinter.CTkButton(self.header,
                                                      text="X",
                                                      width=30,
                                                      fg_color=RED,
                                                      hover_color=DARK_RED,
                                                      command=delete_item
                                                      )
        self.destroy_button.grid(row=0, column=1, sticky="e")

        # Description
        #===========================================================================
        self.description = customtkinter.CTkLabel(self, text=element.get_description())
        self.description.grid(row=1, column=0, padx=10)

        # Power states sub frame
        #===========================================================================
        self.power_state_frame = customtkinter.CTkFrame(self)
        self.power_state_frame.grid(row=2, column=0, padx=10, sticky="nsew")
        self.power_state_frame.grid_rowconfigure(1, weight=0)
        self.power_state_frame.grid_columnconfigure(0, weight=0)
        # Power state
        self.power_states = []
        self.power_states.append(PowerStateFrame(self.power_state_frame,
                                           power_state=element.get_power_state("Wake"),
                                           name="Wake",
                                           color=WAKE_COLOR)
                                           )
        self.power_states[0].grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ne")
        self.power_states.append(PowerStateFrame(self.power_state_frame,
                                            power_state=element.get_power_state("Active"),
                                            name="Active",
                                            color=ACTIVE_COLOR)
                                            )
        self.power_states[1].grid(row=0, column=1, padx=PADX, pady=PADY, sticky="nw")
        self.power_states.append(PowerStateFrame(self.power_state_frame,
                                            power_state=element.get_power_state("Fall"),
                                            name="Fall",
                                            color=IDLE_COLOR)
                                            )
        self.power_states[2].grid(row=1, column=0, padx=PADX, pady=PADY, sticky="se")
        self.power_states.append(PowerStateFrame(self.power_state_frame,
                                            power_state=element.get_power_state("Sleep"),
                                            name="Sleep",
                                            color=SLEEP_COLOR)
                                            )
        self.power_states[3].grid(row=1, column=1, padx=PADX, pady=PADY, sticky="sw")



class PowerStateFrame(customtkinter.CTkFrame):
    def __init__(self, master, power_state: PowerState=None, color="white", name: str="", **kwargs):
        if power_state is None:
            raise ValueError("Power state must be provided")
        super().__init__(master, border_width=1, **kwargs)
        # Attributes
        #===========================================================================
        self.power_state = power_state
        self.color = color

        # configure windows
        #===========================================================================
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(1, weight=0)

        # Power state name
        #===========================================================================
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=0, padx=10)

        # Power state values power
        #===========================================================================
        self.entry_power = customtkinter.StringVar(value=f2s(power_state.get_power()))
        self.entry_power.trace_add("write", self.update_power)

        self.power_label = customtkinter.CTkLabel(self, text="Power (W):")
        self.power_label.grid(row=1, column=0, padx=4)
        self.power = customtkinter.CTkEntry(self,
                                            textvariable=self.entry_power,
                                            width=65,
                                            fg_color=self.color
                                            )
        self.power.grid(row=1, column=1)

        # Power state values time
        #===========================================================================
        self.entry_time = customtkinter.StringVar(value=f2s(power_state.get_time()))
        self.entry_time.trace_add("write", self.update_time)

        self.time_label = customtkinter.CTkLabel(self, text="Time (s):")
        self.time_label.grid(row=2, column=0, padx=4)
        self.time = customtkinter.CTkEntry(self,
                                            textvariable=self.entry_time,
                                            width=65
                                            )
        self.time.grid(row=2, column=1)
    
    # Methods
    #===========================================================================
    def update_power(self, *args):
        self.power.configure(fg_color="white")
        if self.entry_power.get() != "":
            try:
                self.power_state.set_power(s2f(self.entry_power.get()))
            except ValueError:
                self.power_state.set_power(0)
                self.entry_power.set(0)
                self.power.configure(fg_color="red")
        else:
            self.power_state.set_power(0)

    def update_time(self, *args):
        self.time.configure(fg_color="white")
        if self.entry_time.get() != "":
            try:
                self.power_state.set_time(s2f(self.entry_time.get()))
            except ValueError:
                self.power_state.set_time(0)
                self.entry_time.set(0)
                self.time.configure(fg_color="red")
        else:
            self.power_state.set_time(0)

