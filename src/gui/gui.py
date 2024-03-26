# File: gui.py
"""
This file contains the GUI class
"""

# Built-in
import logging
import customtkinter

# App logic
from src.app import App
from src.sequence import Sequence
from src.state import State
from src.elements import Element
from src.power_state import PowerState

# Misc
from src.utils import s2f, f2s

#================================================================================================
# Appearance
#================================================================================================

# Window size
WINDOWS_WIDTH = 1280
WINDOWS_HEIGHT = 720

# UI colors
RED = "#e64040"
DARK_RED = "#d13d3d"

# Power states colors
WAKE_COLOR = "#8deba0"
SLEEP_COLOR = "#eb8d8d"
IDLE_COLOR = "#ebe88d"
ACTIVE_COLOR = "#8dc7eb"

# customtkinter appearance
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")



class GUI(customtkinter.CTk):
    def __init__(self, app: App = App()):
        super().__init__()
        self.app = app
        # Configure windows
        #================================
        self.geometry(f"{WINDOWS_WIDTH}x{WINDOWS_HEIGHT}")
        self.title("Sensor network designer")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=320)

        # Sequences
        #================================
        #self.SequencePannel = SequencePannel(self, dict_sequence=self.app.dict_seqs)
        #self.SequencePannel.grid(row=0, column=0, sticky="new")

        # Graphs
        #================================
        #self.GraphPannel = GraphPannel(self, app=self.app)
        #self.GraphPannel.grid(row=1, column=0, sticky="swne")

        # Elements
        #================================
        self.__pannel_element = PannelElement(master=self, app=self.app)
        self.__pannel_element.grid(row=0, column=1, rowspan=2, sticky="senw", padx=2)


#================================================================================================
# BaseGUIClass
#================================================================================================

class AppGUIInterface:
    def __init__(self, app: App=None):
        if app is None:
            raise ValueError("App must be provided")
        # Attributes
        #================================
        self.app = app
    
    # Getters
    #================================
    def get_app_current_sequence(self) -> Sequence:
        return self.app.current_sequence
    
    def get_app_list_sequence(self) -> list[Sequence]:
        return self.app.loaded_seqs
    
    def get_app_list_elements(self) -> list[Element]:
        return self.app.loaded_elts

    def get_app_sequence(self, name: str) -> Sequence:
        return self.app.dict_seqs[name]

    def get_app_element(self, name: str) -> Element:
        return self.app.dict_elts[name]

    # Setters
    #================================
    def set_app_current_sequence(self, name: str):
        self.app.set_current_sequence(name)
    
    # Create instances
    #================================
    def create_app_sequence(self) -> Sequence:
        return self.app.create_sequence()
    
    def create_app_element(self) -> Element:
        return self.app.create_element()

#================================================================================================
# PannelElement Classes
#================================================================================================

class PannelElement(AppGUIInterface, customtkinter.CTkFrame):
    def __init__(self, master, app: App=None):
        super().__init__(app=app, master=master)
        # Attributes
        #================================

        # Configure windows
        #================================
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Header
        #================================
        self.__header = PannelHeaderElement(self, app=self.app)
        self.__header.grid(row=0, column=0, sticky="nsew")

        # Scrollable elements
        #================================
        self.__scrollableElements = PannelScrollableElement(self, app=self.app)
        self.__scrollableElements.grid(row=1, column=0, sticky="nsew")
    # Methods
    #================================

class PannelHeaderElement(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None, **kwargs):
        super().__init__(master, app, **kwargs)
        # Configure windows
        #================================
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Title pannel
        #================================
        self.name = customtkinter.CTkLabel(self,
                                        text="Available elements",
                                        bg_color="gray",
                                        padx=10
                                        )
        self.name.grid(row=0, column=0)

        # Add create element button
        #================================
        self.add_button = customtkinter.CTkButton(self, text="Add element", command=self.create_element)
        self.add_button.grid(row=0, column=2, sticky="e")

    # Methods
    #================================
    def create_element(self):
        logging.debug("Creating new element")
        CreateElement(self.master)

class PannelScrollableElement(customtkinter.CTkScrollableFrame, AppGUIInterface):
    def __init__(self, master, app: App=None, **kwargs):
        super().__init__(master, app, **kwargs)
        # Attributes
        #================================
        self.__elt_list = self.b_get_list_elements()
        self.__elt_frames = []
        self.__PADX = 2
        self.__PADY = 2

        # configure windows
        #================================
        self.grid_columnconfigure(0, weight=0)

        # Add elements
        #================================
        for elt in self.__elt_list:
            self.add_element(elt)

    # Methods
    #================================
    def add_element(self, index: int=None):
        elt_frame = FrameElement(self, self.app, index=index)
        elt_frame.grid(row=len(self.__elt_frames), column=0, padx=self.PADX, pady=self.PADY, sticky="nsew")
        self.__elt_frames.append(__elt_frame)
        
class FrameElement(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None, index: int=None, **kwargs):
        if index is None:
            raise ValueError("Index must be provided")
        super().__init__(master, app, border_width=1, **kwargs)
        # Attributes
        #================================
        self.__index = index
        self.__element = self.b_get_element(self.__index)
        PADX = 2
        PADY = 2

        # Configure windows
        #================================
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=0)

        # Configure header
        #================================
        self.__header = customtkinter.CTkFrame(self)
        self.__header.grid(row=0, column=0, padx=10, sticky="nsew")
        self.__header.grid_columnconfigure(0, weight=1)
        self.__header.grid_columnconfigure(1, weight=0)

        # Element name
        #================================
        self.__name = customtkinter.CTkLabel(self.header, text=__element.get_name())
        self.__name.grid(row=0, column=0, padx=10, sticky="w")

        # Delete button
        #================================
        def __delete_item():
            logging.debug(f"Deleting {__element.get_name()}")
            self.destroy()
            master.elt_frames.remove(self)
        self.__destroy_button = customtkinter.CTkButton(self.header,
                                                      text="X",
                                                      width=30,
                                                      fg_color=RED,
                                                      hover_color=DARK_RED,
                                                      command=__delete_item
                                                      )
        self.__destroy_button.grid(row=0, column=1, sticky="e")

        # Description
        #================================
        self.__lbl_description = customtkinter.CTkLabel(self, text=__element.get_description())
        self.__lbl_description.grid(row=1, column=0, padx=10)

        # Power states sub frame
        #================================
        self.__power_state_frame = customtkinter.CTkFrame(self)
        self.__power_state_frame.grid(row=2, column=0, padx=10, sticky="nsew")
        self.__power_state_frame.grid_rowconfigure(1, weight=0)
        self.__power_state_frame.grid_columnconfigure(0, weight=0)
        # Power state
        self.__power_states = []
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                           power_state=__element.get_power_state("Wake"),
                                           name="Wake",
                                           color=WAKE_COLOR)
                                           )
        self.__power_states[0].grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ne")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=__element.get_power_state("Active"),
                                            name="Active",
                                            color=ACTIVE_COLOR)
                                            )
        self.__power_states[1].grid(row=0, column=1, padx=PADX, pady=PADY, sticky="nw")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=__element.get_power_state("Fall"),
                                            name="Fall",
                                            color=IDLE_COLOR)
                                            )
        self.__power_states[2].grid(row=1, column=0, padx=PADX, pady=PADY, sticky="se")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=__element.get_power_state("Sleep"),
                                            name="Sleep",
                                            color=SLEEP_COLOR)
                                            )
        self.__power_states[3].grid(row=1, column=1, padx=PADX, pady=PADY, sticky="sw")

class FramePowerState(customtkinter.CTkFrame):
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
