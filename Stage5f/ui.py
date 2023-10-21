from stack import Stack # Import stack object from stack.py
from abc import ABC, abstractmethod # Import abstract base class and abstract method

class UI(ABC):

    VERSION = "v0.5.5" # Set version

    def __init__(self): # Constructor
        self._ui_stack = Stack() # Create new UI stack (for back buttons)
        self._push_ui_to_stack("home") # Push "home" to stack, represents the home screen first being rendered
    
    def _push_ui_to_stack(self, ui): # Push ui to stack method
        self._ui_stack.push(ui)
    
    def _pop_ui_from_stack(self): # Pop ui from stack method
        return self._ui_stack.pop()
    
    def _get_curr_ui(self): # Get current ui at the top of the stack
        return self._ui_stack.peek()

    @abstractmethod
    def run(self): # Run method to start the game, must be implemented by children classes
        raise NotImplementedError