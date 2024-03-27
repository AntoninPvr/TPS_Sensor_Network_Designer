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
from src.battery import Battery

# Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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

POWER_STATE_COLOR = {
    "Wake": WAKE_COLOR,
    "Sleep": SLEEP_COLOR,
    "Fall": IDLE_COLOR,
    "Active": ACTIVE_COLOR
}

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
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=320)

        # Sequences
        #================================
        self.__SequencePannel = PannelSequence(self, self.app)
        self.__SequencePannel.grid(row=0, column=0, columnspan=2, sticky="new")

        # Battery
        #================================
        self.__battery = PannelBattery(self, app=self.app)
        self.__battery.grid(row=1, column=0, sticky="nsew")

        # Graphs
        #================================
        self.__GraphPannel = PannelGraph(self, app=self.app)
        self.__GraphPannel.grid(row=1, column=1, sticky="swne")

        # Elements
        #================================
        self.__pannel_element = PannelElement(self, self.app)
        self.__pannel_element.grid(row=0, column=2, rowspan=2, sticky="senw", padx=2)


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
    # Current sequence
    def get_app_current_sequence(self) -> Sequence:
        return self.app.current_sequence
    
    def get_app_current_sequence_name(self) -> str:
        return self.app.current_sequence.get_name()
    
    def get_app_current_sequence_description(self) -> str:
        return self.app.current_sequence.get_description()
    
    def get_app_current_states(self) -> list[State]:
        return self.app.current_sequence.states
    
    # Sequences
    def get_app_list_sequence(self) -> list[Sequence]:
        return self.app.loaded_seqs
    
    def get_app_sequence_key(self) -> list[str]:
        return list(self.app.dict_seqs.keys())
    
    def get_app_sequence(self, name: str) -> Sequence:
        return self.app.dict_seqs[name]

    # Elements
    def get_app_list_elements(self) -> list[Element]:
        return self.app.loaded_elts

    def get_app_element(self, name: str) -> Element:
        return self.app.dict_elts[name]
    
    # Battery
    def get_app_battery(self) -> Battery:
        return self.app.battery
    
    def get_app_battery_name(self) -> str:
        return self.app.battery.get_name()
    
    def get_app_battery_capacity(self) -> float:
        return self.app.battery.get_capacity()
    
    def get_app_battery_input_power(self) -> float:
        return self.app.battery.get_input_power()
    
    def get_app_battery_max_output_power(self) -> float:
        return self.app.battery.get_max_output_power()
    
    def get_app_battery_efficiency(self) -> float:
        return self.app.battery.get_efficiency()
    
    def get_app_battery_current_capacity(self) -> float:
        return self.app.battery.get_current_capacity()

    # Setters
    #================================
    def set_app_current_sequence(self, name: str):
        self.app.set_current_sequence(name)
    
    # Battery
    def set_app_battery_name(self, name: str):
        self.app.battery.set_name(name)

    def set_app_battery_capacity(self, capacity: float):
        self.app.battery.set_capacity(capacity)

    def set_app_battery_input_power(self, input_power: float):
        self.app.battery.set_input_power(input_power)
    
    def set_app_battery_max_output_power(self, max_output_power: float):
        self.app.battery.set_max_output_power(max_output_power)

    def set_app_battery_efficiency(self, efficiency: float):
        self.app.battery.set_efficiency(efficiency)
    
    def set_app_battery_current_capacity(self, current_capacity: float):
        self.app.battery.set_current_capacity(current_capacity)

    # Create instances
    #================================
    def create_app_sequence(self) -> Sequence:
        return self.app.create_sequence()
    
    def create_app_element(self) -> Element:
        return self.app.create_element()
    
    def create_app_state(self) -> State:
        return self.app.create_state()

    # Removers
    #================================
    def remove_app_element(self, element: Element):
        self.app.remove_element(element)

    def remove_app_sequence(self, sequence: Sequence):
        self.app.remove_sequence(sequence)

    def remove_app_sequence_and_back_to_last(self, sequence: Sequence):
        self.app.remove_sequence(sequence)
        last_key = list(self.app.dict_seqs.keys())[-1]
        self.app.current_sequence = self.app.dict_seqs[last_key]

    def remove_app_state(self, state: State, sequence: Sequence=None):
        if sequence is None:
            sequence = self.app.current_sequence
        self.app.remove_state(state, sequence)

    # Adders
    #================================
    def add_app_sequence(self, sequence: Sequence):
        self.app.add_sequence(sequence)

#================================================================================================
# PannelElement Classes
#================================================================================================

class PannelElement(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None,):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)
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
        self.__scrollable_elements = PannelScrollableElement(self, app=self.app)
        self.__scrollable_elements.grid(row=1, column=0, sticky="nsew")

    # Methods
    #================================
    def update_scollable_elements(self):
        self.__scrollable_elements.update_scollable_elements()

class PannelHeaderElement(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)
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
        WinCreateElement(self, self.app)

class PannelScrollableElement(customtkinter.CTkScrollableFrame, AppGUIInterface):
    def __init__(self, master, app: App=None, **kwargs):
        customtkinter.CTkScrollableFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)
        # Attributes
        #================================
        self.__elt_list = self.get_app_list_elements()
        self.__elt_frames: list[FrameElement] = []
        self.__PADX = 2
        self.__PADY = 2

        # configure windows
        #================================
        self.grid_columnconfigure(0, weight=0)

        # Add elements
        #================================
        self.update_scollable_elements()

    # Methods
    #================================
    def add_hidden_element(self):
        for elt in self.__elt_list:
            if elt.get_name() not in [frame.get_name() for frame in self.__elt_frames]:
                elt_frame = FrameElement(self, self.app, elt_name=elt.get_name())
                elt_frame.grid(row=len(self.__elt_frames), column=0, padx=self.__PADX, pady=self.__PADY, sticky="nsew")
                self.__elt_frames.append(elt_frame)
            
    def remove_obsolete_element(self):
        for frame in self.__elt_frames:
            if frame.get_name() not in [elt.get_name() for elt in self.__elt_list]:
                frame.destroy()
                self.__elt_frames.remove(frame)

    def update_scollable_elements(self):
        self.remove_obsolete_element()
        self.add_hidden_element()

class FrameElement(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None, elt_name: int=None, **kwargs):
        if elt_name is None:
            raise ValueError("Index must be provided")
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================
        self.__elt_name = elt_name
        self.__element = self.get_app_element(self.__elt_name)
        self.__master = master
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
        self.__name = customtkinter.CTkLabel(self.__header, text=self.__element.get_name())
        self.__name.grid(row=0, column=0, padx=10, sticky="w")

        # Delete button
        #================================
        def __delete_item():
            logging.debug(f"Deleting {self.__element.get_name()}")
            self.destroy()
            self.remove_app_element(self.__element)
            self.__master.update_scollable_elements()
        
        self.__destroy_button = customtkinter.CTkButton(self.__header,
                                                      text="X",
                                                      width=30,
                                                      fg_color=RED,
                                                      hover_color=DARK_RED,
                                                      command=__delete_item
                                                      )
        self.__destroy_button.grid(row=0, column=1, sticky="e")

        # Description
        #================================
        self.__lbl_description = customtkinter.CTkLabel(self, text=self.__element.get_description())
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
                                           power_state=self.__element.get_power_state("Wake"),
                                           name="Wake",
                                           color=WAKE_COLOR)
                                           )
        self.__power_states[0].grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ne")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=self.__element.get_power_state("Active"),
                                            name="Active",
                                            color=ACTIVE_COLOR)
                                            )
        self.__power_states[1].grid(row=0, column=1, padx=PADX, pady=PADY, sticky="nw")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=self.__element.get_power_state("Fall"),
                                            name="Fall",
                                            color=IDLE_COLOR)
                                            )
        self.__power_states[2].grid(row=1, column=0, padx=PADX, pady=PADY, sticky="se")
        self.__power_states.append(FramePowerState(self.__power_state_frame,
                                            power_state=self.__element.get_power_state("Sleep"),
                                            name="Sleep",
                                            color=SLEEP_COLOR)
                                            )
        self.__power_states[3].grid(row=1, column=1, padx=PADX, pady=PADY, sticky="sw")

    # Methods
    #================================
    
    # Getters
    #================================
    def get_name(self) -> str:
        return self.__element.get_name()

class FramePowerState(customtkinter.CTkFrame):
    def __init__(self, master, power_state: PowerState=None, color="white", name: str="", **kwargs):
        if power_state is None:
            raise ValueError("Power state must be provided")
        customtkinter.CTkFrame.__init__(self, master, border_width=1)
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

class WinCreateElement(customtkinter.CTkToplevel, AppGUIInterface):
    def __init__(self, master, app: App=None, **kwargs):
        customtkinter.CTkToplevel.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #===========================================================================
        self.element = self.create_app_element()

        # configure windows
        #===========================================================================
        self.grab_set()
        self.title("Create new element")
        self.geometry("350x350")

        # Create element frame
        #===========================================================================
        self.frame_create_element_sub = CreateElementSub(self, element=self.element)
        self.frame_create_element_sub.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Cancel button
        #===========================================================================
        self.cancel_button = customtkinter.CTkButton(self,
                                                    text="Cancel",
                                                    width=60,
                                                    fg_color=RED,
                                                    hover_color=DARK_RED,
                                                    command=self.cancel
                                                    )
        self.cancel_button.grid(row=1, column=0, sticky="w")

        # Save button
        #===========================================================================
        self.save_button = customtkinter.CTkButton(self,
                                                    text="Save",
                                                    width=60,
                                                    command=self.save
                                                    )
        self.save_button.grid(row=1, column=1, sticky="e")
    # Methods
    #===========================================================================
    def cancel(self):
        logging.debug("Canceling element creation")
        self.destroy()

    def save(self):
        logging.debug("Saving element")
        self.frame_create_element_sub.save()
        if not self.element.get_name() == "":
            self.app.add_element(self.element)
            self.master.master.update_scollable_elements()
            self.destroy()
        else:
            self.frame_create_element_sub.name_warning()
            logging.error("Element name is empty")

class CreateElementSub(customtkinter.CTkFrame):
    def __init__(self, master, element=None, **kwargs):
        if element is None:
            raise ValueError("Element must be provided")
        customtkinter.CTkFrame.__init__(self, master)
        # Attributes
        #===========================================================================
        self.element = element
        PADX = 2
        PADY = 2

        # configure windows
        #===========================================================================
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        #===========================================================================
        self.header = customtkinter.CTkFrame(self)
        self.header.grid(row=0, column=0, padx=10, sticky="nsew")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0)

        # Element name
        self.name = customtkinter.CTkEntry(self.header, placeholder_text="name", width=100)
        self.name.grid(row=0, column=0, padx=10, sticky="w")

        # Description
        self.description = customtkinter.CTkTextbox(self, width=300, height=100)
        self.description.grid(row=1, column=0, padx=10)

        # Power states sub frame
        #===========================================================================
        self.power_state_frame = customtkinter.CTkFrame(self)
        self.power_state_frame.grid(row=2, column=0, padx=10, sticky="nsew")
        self.power_state_frame.grid_rowconfigure(1, weight=0)
        self.power_state_frame.grid_columnconfigure(0, weight=0)
        # Power state
        self.power_states = []
        self.power_states.append(FramePowerState(self.power_state_frame,
                                           power_state=element.get_power_state("Wake"),
                                           name="Wake")
                                           )
        self.power_states[0].grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ne")
        self.power_states.append(FramePowerState(self.power_state_frame,
                                           power_state=element.get_power_state("Active"),
                                           name="Active")
                                           )
        self.power_states[1].grid(row=0, column=1, padx=PADX, pady=PADY, sticky="nw")
        self.power_states.append(FramePowerState(self.power_state_frame,
                                           power_state=element.get_power_state("Fall"),
                                           name="Fall")
                                           )
        self.power_states[2].grid(row=1, column=0, padx=PADX, pady=PADY, sticky="se")
        self.power_states.append(FramePowerState(self.power_state_frame,
                                           power_state=element.get_power_state("Sleep"),
                                           name="Sleep")
                                           )
        self.power_states[3].grid(row=1, column=1, padx=PADX, pady=PADY, sticky="sw")

    # Methods
    #===========================================================================
    def save(self):
        logging.debug("Saving element")
        self.element.set_name(self.name.get())
        self.element.set_description(self.description.get(1.0, "end"))

    def name_warning(self):
        self.name.configure(fg_color="red")

#================================================================================================
# PannelSequence Classes
#================================================================================================

class PannelSequence(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master, height=200)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Selection frame
        #================================
        self.__selection_frame = PannelSelectionSequence(self, self.app)
        self.__selection_frame.grid(row=0, column=0, sticky="nsew")

        # Scrollable frame
        #================================
        self.__scrollable_frame = PannelScrollableSequence(self, self.app)
        self.__scrollable_frame.grid(row=0, column=1, sticky="nsew")

    # Methods
    #================================
    def update_scrollable_state(self):
        self.__scrollable_frame.update_scrollable_state()
    
class PannelScrollableSequence(customtkinter.CTkScrollableFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkScrollableFrame.__init__(self, master, orientation="horizontal")
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================
        self.state_frame = []

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), minsize=150)

        # States
        #================================
        self.update_scrollable_state()

    # Methods
    #================================
    def add_hidden_state(self):
        for state in self.get_app_current_states():
            state_frame = StateFrame(self, state)
            state_frame.grid(row=0, column=len(self.state_frame), sticky="nsew", padx=2)
            self.state_frame.append(state_frame)

    def remove_obsolete_state(self):
        length = len(self.state_frame)
        for i in range(length):
            self.state_frame[i].destroy()
        self.state_frame = []

    def update_scrollable_state(self):
        self.remove_obsolete_state()
        self.add_hidden_state()

    def remove_state(self, state: State):
        self.remove_app_state(state)
        self.update_scrollable_state()

class StateFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, state: State=None):
        if state is None:
            raise ValueError("State must be provided")
        super().__init__(master, border_width=1)
        # Attributes
        #================================
        self.master = master
        self.state = state
        self.elements_frame = []

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Header
        #================================
        self.header = customtkinter.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.header.grid_columnconfigure(1, weight=1)

        # Shift left
        self.add_left_button = customtkinter.CTkButton(self.header,
                                                    text="<",
                                                    width=30,
                                                    command=self.shift_left
                                                    )
        self.add_left_button.grid(row=0, column=0, sticky="w")

        # Name
        self.name = customtkinter.CTkLabel(self.header,
                                           text=self.state.get_name()
                                           )
        self.name.grid(row=0, column=1, sticky="we")

        # Description
        #================================
        self.description = customtkinter.CTkLabel(self,
                                                    width=100,
                                                    height=50,
                                                    text=self.state.get_description()
                                                    )
        self.description.grid(row=1, column=0, columnspan=2, sticky="we")

        # Delete button
        self.delete_button = customtkinter.CTkButton(self.header,
                                                    text="X",
                                                    width=30,
                                                    command=self.delete_state,
                                                    fg_color=RED,
                                                    hover_color=DARK_RED
                                                    )
        self.delete_button.grid(row=0, column=2, sticky="e")

        # Add right button
        self.add_right_button = customtkinter.CTkButton(self.header,
                                                    text=">",
                                                    width=30,
                                                    command=self.shift_right
                                                    )
        self.add_right_button.grid(row=0, column=3, sticky="e")

        # Elements
        #================================
        for i, elt in enumerate(self.state.elements):
            self.elements_frame.append(ElementSubState(self, elt["element"], elt["power_state"]))
            self.elements_frame[i].grid(row=i+2, column=0, sticky="nsew")

    # Methods
    #================================
    def shift_left(self):
        pass
    
    def shift_right(self):
        pass

    def delete_state(self):
        self.master.remove_state(self.state)


class ElementSubState(customtkinter.CTkFrame):
    def __init__(self, master, element: Element=None, power_state: PowerState=None):
        if element is None:
            raise ValueError("Element must be provided")
        if power_state is None:
            raise ValueError("Power state must be provided")
        super().__init__(master)

        # Attributes
        #================================
        self.element = element
        self.power_state = power_state

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Element name
        #================================
        self.label_name = customtkinter.CTkLabel(self,
                                           text=self.element.get_name(),
                                           padx=4,
                                           fg_color=POWER_STATE_COLOR[self.power_state]
                                           )
        self.label_name.grid(row=0, column=0, sticky="w")

        # Power state
        #================================
        self.label_power_state = customtkinter.CTkLabel(self,
                                                    text=self.power_state,
                                                    padx=10,
                                                    fg_color=POWER_STATE_COLOR[self.power_state]
                                                    )
        self.label_power_state.grid(row=0, column=1, sticky="e")

        # Power consumption
        #================================
        self.power_frame = customtkinter.CTkFrame(self)
        self.power_frame.grid(row=1, column=0, sticky="nsew")
        text_power = customtkinter.StringVar(value=f2s(self.element.get_power(self.power_state)))
        self.label_power = customtkinter.CTkEntry(self.power_frame,
                                                    textvariable=text_power,
                                                    width=65,
                                                    state="disabled"
                                                    )
        self.label_power.grid(row=0, column=0, sticky="w")
        self.label_power_name = customtkinter.CTkLabel(self.power_frame,
                                                        text=" W",
                                                        )
        self.label_power_name.grid(row=0, column=1, sticky="w")

        # Time
        #================================
        self.time_frame = customtkinter.CTkFrame(self)
        self.time_frame.grid(row=1, column=1, padx=10)
        text_time = customtkinter.StringVar(value=f2s(self.element.get_time(self.power_state)))
        self.label_time = customtkinter.CTkEntry(self.time_frame,
                                                    textvariable=text_time,
                                                    width=65,
                                                    state="disabled"
                                                    )
        self.label_time.grid(row=0, column=0, sticky="e")
        self.label_time_name = customtkinter.CTkLabel(self.time_frame,
                                                    text=" s",
                                                    )
        self.label_time_name.grid(row=0, column=1, sticky="e")

class PannelSelectionSequence(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        # Label pannel
        #================================
        self.label = customtkinter.CTkLabel(self,
                                            text="Available sequences",
                                            bg_color="gray",
                                            padx=10
                                            )
        self.label.grid(row=0, column=0)

        # Selection frame
        #================================
        self.selection_frame = customtkinter.CTkFrame(self)
        self.selection_frame.grid(row=1, column=0, sticky="nsew")

        # Sequence selection
        self.sequence_selection = customtkinter.CTkComboBox(self.selection_frame,
                                                            values=self.get_app_sequence_key(),
                                                            command=self.selection_sequence
                                                            )
        self.sequence_selection.set(self.get_app_current_sequence_name())
        self.sequence_selection.grid(row=0, column=0, columnspan=2)

        # Delete button
        self.delete_button = customtkinter.CTkButton(self.selection_frame,
                                                    text="Delete",
                                                    width=60,
                                                    fg_color=RED,
                                                    hover_color=DARK_RED,
                                                    command=self.delete_sequence
                                                    )
        self.delete_button.grid(row=1, column=0, sticky="nw")

        # Add button
        self.add_button = customtkinter.CTkButton(self.selection_frame,
                                                text="Add",
                                                width=60,
                                                command=self.add_sequence
                                                )
        self.add_button.grid(row=1, column=1, sticky="ne")

        # Sequence edition
        #================================
        self.sequence_edition = customtkinter.CTkFrame(self)
        self.sequence_edition.grid(row=2, column=0)

        # Description
        self.label_description = customtkinter.CTkLabel(self.sequence_edition, text=self.get_app_current_sequence_description(), height=50)
        self.label_description.grid(row=0, column=0)

        # Add state button
        self.add_state_button = customtkinter.CTkButton(self.sequence_edition,
                                                        text="Add state",
                                                        command=self.add_state
                                                        )
        self.add_state_button.grid(row=1, column=0)

    # Methods
    #================================
    def selection_sequence(self, *args):
        self.set_app_current_sequence(self.sequence_selection.get())
        self.label_description.configure(text=self.get_app_current_sequence_description())
        self.update_scrollable_state()

    def delete_sequence(self):
        self.remove_app_sequence_and_back_to_last(self.get_app_current_sequence())
        self.update_selection()
        self.update_scrollable_state()

    def add_sequence(self):
        WinCreateSequence(self, self.app)

    def update_selection(self):
        self.sequence_selection.configure(values=self.get_app_sequence_key())
        self.sequence_selection.set(self.get_app_current_sequence_name())
        self.label_description.configure(text=self.get_app_current_sequence_description())  
    
    def add_state(self):
        WinCreateState(self, self.app)
    
    def update_scrollable_state(self):
        self.master.update_scrollable_state()

class WinCreateSequence(customtkinter.CTkToplevel, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkToplevel.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # configure windows
        #================================
        self.grab_set()
        self.geometry("300x300")
        self.title("Create sequence")

        # Name
        #================================
        self.name = customtkinter.CTkEntry(self, placeholder_text="Name", width=100)
        self.name.grid(row=0, column=0, columnspan=2)

        # Description
        #================================
        self.description = customtkinter.CTkTextbox(self, width=300, height=100)
        self.description.grid(row=1, column=0, columnspan=2)

        # Cancel button
        #================================
        self.cancel_button = customtkinter.CTkButton(self,
                                                    text="Cancel",
                                                    width=60,
                                                    fg_color=RED,
                                                    hover_color=DARK_RED,
                                                    command=self.cancel
                                                    )
        self.cancel_button.grid(row=2, column=0, sticky="w")

        # Save button
        #================================
        self.save_button = customtkinter.CTkButton(self,
                                                    text="Save",
                                                    width=60,
                                                    command=self.save
                                                    )
        self.save_button.grid(row=2, column=1, sticky="e")

    # Methods
    #================================
    def cancel(self):
        logging.debug("Canceling element creation")
        self.destroy()

    def save(self):
        logging.debug("Saving element")
        name = self.name.get()

        if not name == "":
            self.sequence = self.create_app_sequence()
            self.sequence.set_name(name)
            self.sequence.set_description(self.description.get(1.0, "end"))
            self.add_app_sequence(self.sequence)
            self.set_app_current_sequence(name)
            self.master.update_selection()
            self.master.master.update_scrollable_state()
            self.destroy()
            logging.info(f"Sequence {self.sequence.get_name()} created")   
        else:
            self.name.configure(fg_color="red")
            logging.error("Name is empty")

class WinCreateState(customtkinter.CTkToplevel, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkToplevel.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #===========================================================================

        # configure windows
        #===========================================================================
        self.grab_set()
        self.geometry("600x600")
        self.title("Create state")

        # Name
        #===========================================================================
        self.name = customtkinter.CTkEntry(self, placeholder_text="Name", width=100)
        self.name.grid(row=0, column=0, columnspan=2)
        # Description
        #===========================================================================
        self.description = customtkinter.CTkTextbox(self, width=600, height=100)
        self.description.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Elements choice
        #===========================================================================
        self.elements_choice = ElementChoice(self, self.app)
        self.elements_choice.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Cancel button
        #===========================================================================
        self.cancel_button = customtkinter.CTkButton(self,
                                                    text="Cancel",
                                                    width=60,
                                                    fg_color=RED,
                                                    hover_color=DARK_RED,
                                                    command=self.cancel
                                                    )
        self.cancel_button.grid(row=3, column=0, sticky="w")

        # Save button
        #===========================================================================
        self.save_button = customtkinter.CTkButton(self,
                                                    text="Save",
                                                    width=60,
                                                    command=self.save
                                                    )
        self.save_button.grid(row=3, column=1, sticky="e")

    # Methods
    #===========================================================================
    def cancel(self):
        logging.debug("Canceling element creation")
        self.destroy()

    def save(self):
        logging.debug("Saving element")
        name = self.name.get()

        if not name == "":
            self.state = self.create_app_state()
            self.state.set_name(name)
            self.state.elements = self.elements_choice.save()
            self.state.set_description(self.description.get(1.0, "end"))

            self.get_app_current_sequence().add_state(self.state)
            self.master.update_scrollable_state()
            self.destroy()
            logging.info(f"State {self.state.get_name()} created")
        else:
            self.name.configure(fg_color="red")
            logging.error("Name is empty")

class ElementChoice(customtkinter.CTkScrollableFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkScrollableFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #===========================================================================
        self.elements_frame = []

        # configure windows
        #===========================================================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Elements
        #===========================================================================
        for i, elt in enumerate(self.get_app_list_elements()):
            self.elements_frame.append(ElementConf(self, elt))
            self.elements_frame[i].grid(row=i, column=0, sticky="nsew")
    
    # Methods
    #===========================================================================
    def save(self):
        list_elements = []
        for elt_conf in self.elements_frame:
            elt, power_state = elt_conf.save()
            list_elements.append({"element": elt, "power_state": power_state})
        return list_elements

class ElementConf(customtkinter.CTkFrame):
    def __init__(self, master, element: Element=None):
        if element is None:
            raise ValueError("Element must be provided")
        super().__init__(master)
        # Attributes
        #===========================================================================
        self.element = element

        # configure windows
        #===========================================================================
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Element name
        #===========================================================================
        self.label_name = customtkinter.CTkLabel(self,
                                           text=self.element.get_name(),
                                           padx=4,
                                           )
        self.label_name.grid(row=0, column=0, sticky="w")

        # Power mode
        #===========================================================================
        self.radio_var = customtkinter.StringVar(value="Sleep")
        self.radio_wake = customtkinter.CTkRadioButton(self,
                                                    text="Wake",
                                                    variable=self.radio_var,
                                                    value="Wake",
                                                    bg_color=POWER_STATE_COLOR["Wake"]
                                                    )
        self.radio_wake.grid(row=0, column=1, sticky="w")
        self.radio_active = customtkinter.CTkRadioButton(self,
                                                    text="Active",
                                                    variable=self.radio_var,
                                                    value="Active",
                                                    bg_color=POWER_STATE_COLOR["Active"]
                                                    )
        self.radio_active.grid(row=0, column=2, sticky="w")
        self.radio_fall = customtkinter.CTkRadioButton(self,
                                                    text="Fall",
                                                    variable=self.radio_var,
                                                    value="Fall",
                                                    bg_color=POWER_STATE_COLOR["Fall"]
                                                    )
        self.radio_fall.grid(row=0, column=3, sticky="w")
        self.radio_sleep = customtkinter.CTkRadioButton(self,
                                                    text="Sleep",
                                                    variable=self.radio_var,
                                                    value="Sleep",
                                                    bg_color=POWER_STATE_COLOR["Sleep"]
                                                    )
        self.radio_sleep.grid(row=0, column=4, sticky="w")

    # Methods
    #===========================================================================
    def save(self):
        return self.element, self.radio_var.get()
    
#================================================================================================
# PannelGraph Classes
#================================================================================================
    
class PannelGraph(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # configure windows
        #================================
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        #================================
        self.__header = PannelHeaderGraph(self, app=self.app)
        self.__header.grid(row=0, column=0, sticky="nsew")

        # Graph
        #================================
        self.__graph = Graph(self, app=self.app)
        self.__graph.grid(row=1, column=0, sticky="nsew")

class Graph(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # configure windows
        #================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Graph
        #================================
        self.__graph = customtkinter.CTkFrame(self)
        self.__graph.grid(row=0, column=0, sticky="nse")

        # Add data
        #================================
        self.__fig = Figure(figsize=(7, 4), dpi=100)

        self.y = [i**2 for i in range(101)] 
        self.plot1 = self.__fig.add_subplot(111)
        self.plot1.plot(self.y)
        self.plot1.set_title("Power consumption")
        self.plot1.set_xlabel("Time")
        self.plot1.set_ylabel("Power (W)")
        self.__fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.__fig, master=self.__graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.__graph)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

class PannelHeaderGraph(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # Configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Label pannel
        #================================
        self.__label = customtkinter.CTkLabel(self,
                                            text=f"Sequence graph for {self.get_app_current_sequence_name()}",
                                            bg_color="gray",
                                            padx=10
                                            )
        self.__label.grid(row=0, column=0)
    
    def update(self) -> None:
        self.__label.configure(text=f"Sequence graph for {self.get_app_current_sequence_name()}")

class PannelBattery(customtkinter.CTkFrame, AppGUIInterface):
    def __init__(self, master, app: App=None):
        customtkinter.CTkFrame.__init__(self, master)
        AppGUIInterface.__init__(self, app)

        # Attributes
        #================================

        # Configure windows
        #================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Label pannel
        #================================
        self.__label = customtkinter.CTkLabel(self,
                                            text="Battery",
                                            bg_color="gray",
                                            padx=10
                                            )
        self.__label.grid(row=0, column=0, columnspan=3)

        # Name
        #================================
        self.__label_name = customtkinter.CTkLabel(self,
                                                text=self.get_app_battery_name(),
                                                padx=10
                                                )
        self.__label_name.grid(row=1, column=0)

        # Capacity
        #================================
        self.__label_capacity = customtkinter.CTkLabel(self,
                                                       text="Capacity"
                                                       )
        self.__label_capacity.grid(row=2, column=0)

        self.__capacity = customtkinter.StringVar(value=f2s(self.get_app_battery_capacity()))
        self.__capacity.trace_add("write", self.update_capacity)
        self.__entry_capacity = customtkinter.CTkEntry(self,
                                                    textvariable=self.__capacity,
                                                    width=65
                                                    )
        self.__entry_capacity.grid(row=2, column=1, sticky="ne")

        self.__capacity_unit = customtkinter.CTkLabel(self,
                                                    text="J",
                                                    width=20
                                                    )
        self.__capacity_unit.grid(row=2, column=2, sticky="e")

        # Max power
        #================================
        self.__label_max_power = customtkinter.CTkLabel(self,
                                                       text="Max power"
                                                       )
        self.__label_max_power.grid(row=3, column=0)

        self.__max_power = customtkinter.StringVar(value=f2s(self.get_app_battery_max_output_power()))
        self.__max_power.trace_add("write", self.update_max_power)
        self.__entry_max_power = customtkinter.CTkEntry(self,
                                                    textvariable=self.__max_power,
                                                    width=65
                                                    )
        self.__entry_max_power.grid(row=3, column=1, sticky="ne")

        self.__max_power_unit = customtkinter.CTkLabel(self,
                                                    text="W",
                                                    width=20,
                                                    )
        self.__max_power_unit.grid(row=3, column=2, sticky="e")

        # Input power
        #================================
        self.__label_input_power = customtkinter.CTkLabel(self,
                                                       text="Input power"
                                                       )
        self.__label_input_power.grid(row=4, column=0)

        self.__input_power = customtkinter.StringVar(value=f2s(self.get_app_battery_input_power()))
        self.__input_power.trace_add("write", self.update_input_power)
        self.__entry_input_power = customtkinter.CTkEntry(self,
                                                    textvariable=self.__input_power,
                                                    width=65
                                                    )
        self.__entry_input_power.grid(row=4, column=1, sticky="ne")

        self.__input_power_unit = customtkinter.CTkLabel(self,
                                                    text="W",
                                                    width=20
                                                    )
        self.__input_power_unit.grid(row=4, column=2, sticky="e")

        # Efficiency
        #================================
        self.__label_efficiency = customtkinter.CTkLabel(self,
                                                       text="Efficiency"
                                                       )
        self.__label_efficiency.grid(row=5, column=0)

        self.__efficiency = customtkinter.StringVar(value=f2s(self.get_app_battery_efficiency()))
        self.__efficiency.trace_add("write", self.update_efficiency)
        self.__entry_efficiency = customtkinter.CTkEntry(self,
                                                    textvariable=self.__efficiency,
                                                    width=65
                                                    )
        self.__entry_efficiency.grid(row=5, column=1, sticky="ne")

        self.__efficiency_unit = customtkinter.CTkLabel(self,
                                                    text="%",
                                                    width=20
                                                    )
        self.__efficiency_unit.grid(row=5, column=2, sticky="e")
    
        # Current capacity
        #================================
        self.__label_current_capacity = customtkinter.CTkLabel(self,
                                                       text="Current"
                                                       )
        self.__label_current_capacity.grid(row=6, column=0)

        self.__current_capacity = customtkinter.StringVar(value=f2s(self.get_app_battery_current_capacity()))
        self.__current_capacity.trace_add("write", self.update_current_capacity)
        self.__entry_current_capacity = customtkinter.CTkEntry(self,
                                                    textvariable=self.__current_capacity,
                                                    width=65
                                                    )
        self.__entry_current_capacity.grid(row=6, column=1, sticky="ne")

        self.__current_capacity_unit = customtkinter.CTkLabel(self,
                                                    text="J",
                                                    width=20
                                                    )
        self.__current_capacity_unit.grid(row=6, column=2, sticky="e")

        # Buttons
        #================================
        self.__button_frame = customtkinter.CTkFrame(self)
        self.__button_frame.grid(row=7, column=0, columnspan=3, sticky="nswe")
    
        # Fill Button
        self.__fill_button = customtkinter.CTkButton(self.__button_frame,
                                                    text="Fill battery",
                                                    width=60,
                                                    command=self.fill
                                                    )
        self.__fill_button.grid(row=0, column=0, sticky="w")

        # Update graph Button
        self.__update_graph_button = customtkinter.CTkButton(self.__button_frame,
                                                        text="Update graph",
                                                        width=60,
                                                        command=self.update_graph
                                                        )
        self.__update_graph_button.grid(row=0, column=1, sticky="w")

        # Step state frame
        #================================
        self.__step_state_frame = customtkinter.CTkFrame(self)
        self.__step_state_frame.grid(row=8, column=0, columnspan=3, sticky="nswe")
        
        # State spinbox
        self.__state_spinbox = Spinbox(self.__step_state_frame, step_size=1)
        self.__state_spinbox.grid(row=0, column=0, sticky="w")

        #
    # Methods
    #================================
        
    def update(self):
        self.__capacity.set(f2s(self.get_app_battery_capacity()))
        self.__max_power.set(f2s(self.get_app_battery_max_output_power()))
        self.__input_power.set(f2s(self.get_app_battery_input_power()))
        self.__efficiency.set(f2s(self.get_app_battery_efficiency()))
        self.__current_capacity.set(f2s(self.get_app_battery_current_capacity()))

    def update_capacity(self, *args):
        self.__entry_capacity.configure(fg_color="white")
        if self.__entry_capacity.get() != "":
            try:
                if s2f(self.__entry_capacity.get()) > 0:
                    self.set_app_battery_capacity(s2f(self.__entry_capacity.get()))
                else:
                    raise ValueError("Capacity must be positive")
            except ValueError:
                self.set_app_battery_capacity(0)
                self.__capacity.set(0)
                self.__entry_capacity.configure(fg_color="red")
        else:
            self.set_app_battery_capacity(0)
    
    def update_max_power(self, *args):
        self.__entry_max_power.configure(fg_color="white")
        if self.__entry_max_power.get() != "":
            try:
                if s2f(self.__entry_max_power.get()) > 0:
                    self.set_app_battery_max_output_power(s2f(self.__entry_max_power.get()))
                else:
                    raise ValueError("Max power must be positive")
            except ValueError:
                self.set_app_battery_max_output_power(0)
                self.__max_power.set(0)
                self.__entry_max_power.configure(fg_color="red")
        else:
            self.set_app_battery_max_output_power(0)
    
    def update_input_power(self, *args):
        self.__entry_input_power.configure(fg_color="white")
        if self.__entry_input_power.get() != "":
            try:
                if s2f(self.__entry_input_power.get()) >= 0:
                    self.set_app_battery_input_power(s2f(self.__entry_input_power.get()))
                else:
                    raise ValueError("Max power must be positive")
            except ValueError:
                self.set_app_battery_input_power(0)
                self.__input_power.set(0)
                self.__entry_input_power.configure(fg_color="red")
        else:
            self.set_app_battery_input_power(0)

    def update_efficiency(self, *args):
        self.__entry_efficiency.configure(fg_color="white")
        if self.__entry_efficiency.get() != "":
            try:
                if s2f(self.__entry_efficiency.get()) > 0 and s2f(self.__entry_efficiency.get()) <= 100:
                    self.set_app_battery_efficiency(s2f(self.__entry_efficiency.get()))
                else:
                    raise ValueError("Efficiency must stay between 0 and 100%")
            except ValueError:
                self.set_app_battery_efficiency(100)
                self.__efficiency.set(100)
                self.__entry_efficiency.configure(fg_color="red")
        else:
            self.set_app_battery_efficiency(100)
    
    def update_current_capacity(self, *args):
        self.__entry_current_capacity.configure(fg_color="white")
        if self.__entry_current_capacity.get() != "":
            try:
                if s2f(self.__entry_current_capacity.get()) <= self.get_app_battery_capacity():
                    self.set_app_battery_current_capacity(s2f(self.__entry_current_capacity.get()))
                else:
                    raise ValueError("Current capacity must be bellow full capacity")
            except ValueError:
                self.set_app_battery_current_capacity(0)
                self.__current_capacity.set(0)
                self.__entry_current_capacity.configure(fg_color="red")
        else:
            self.set_app_battery_current_capacity(0)

    def fill(self, *args):
        self.set_app_battery_current_capacity(self.get_app_battery_capacity())
        self.update()
    
    def update_graph(self, *args):
        pass

class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 command = None,
                 **kwargs
                 ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> int:
        try:
            return self.entry.get()
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))