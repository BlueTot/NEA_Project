from board import * # Import everything from board
from board_actions import * # Import everything from board_actions
from generator import BoardGenerator
from solver import BoardSolver
from stack import Stack # Import stack class
from datetime import datetime, timedelta # Import datetime and timedelta functions from datetime
import json # Import json module
import os # Import os module
from copy import deepcopy # Import deepcopy function from copy
from math import floor # Import floor function from math
from rating_calc import * # Import rating calculation details

class GameError(Exception): # GameError exception class
    pass

class Game: # Game class

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Expert"} # Difficulty-number pair for TERMINAL only
    NUM_HINTS = {"Easy": 80, "Medium": 65, "Hard": 50, "Expert": 35} # Number of hints for each difficulty
    DEFAULT_DIRECTORY = "games" # Default directory to save game files
    
    def __init__(self): # Constructor
        self.__action_stack = Stack() # Stack to store user actions
        self.__file = None # File for which game has been loaded from
        self.__creation_date = str(datetime.now().date()) # Creation date
        self.__creation_time = str(datetime.now().time()) # Creation time
        
    def generate(self, mode, difficulty, board_size, timed): # Generate new board method (takes mode : str, difficulty: str, board_size : int, timed: boolean)
        self.__mode = mode # Set mode
        self.__difficulty = difficulty # Set difficulty
        self.__num_of_hints = int(self.NUM_HINTS[self.__difficulty] / 81 * (board_size ** 2)) # Calculate number of hints based on number of squares
        self.__orig_num_of_hints = self.__num_of_hints # Set original number of hints
        self.__board_size = board_size # Set board size
        self.__VALID_NUMS = [i for i in range(1, self.__board_size + 1)] # Set valid numbers depending on board size
        self.__board = BoardGenerator.new_board(self.__mode, self.__difficulty, self.__board_size) # Create the board object
        self.__orig_board = deepcopy(self.__board) # Create orig board object using deepcopy
        self.__timed = timed # Set timed
        self.__time_elapsed = 0 if self.__timed else None # Set time elapsed
    
    @staticmethod
    def get_stats_from(account, file): # Method to get stats of a given file (returns dictionary)
        with open(f"{Game.DEFAULT_DIRECTORY}/{account}/{file}") as f:
            return json.load(f)

    def load_game(self, account, file): # Method to load game from file (takes file : str)

        data = self.get_stats_from(account, file) # Stores as dictionary
        self.__file = file # Set file attribute to file name
        self.__mode = data["mode"] # Set mode
        self.__difficulty = data["difficulty"] # Set difficulty
        self.__num_of_hints = data["num of hints"] # Set number of hints
        self.__orig_num_of_hints = self.__num_of_hints # Set original number of hints
        self.__board_size = data["board size"] # Set board size
        self.__VALID_NUMS = [i for i in range(1, self.__board_size + 1)] # Set valid numbers depending on board size

        # Create null board object
        self.__board = NormalModeBoard(self.__board_size) if self.__mode == "Normal" else KillerModeBoard(self.__board_size)
        self.__orig_board = deepcopy(self.__board) # Deepcopy to get orig board
        
        self.__board.load(data["board"]) # Load null board with squares
        self.__orig_board.load(data["orig board"]) # Load null orig board with squares
        self.__creation_date = data["creation date"] # Set creation date
        self.__creation_time = data["creation time"] # Set creation time
        self.__timed = data["timed"] # Set timed
        self.__time_elapsed = data["time elapsed"] # Set time elapsed
    
    def save_game(self, account): # Save game to file method

        # Create file name based on local time if board is not loaded from a file
        file_name = f"singleplayer_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.json" if self.__file is None else self.__file

        with open(f"{self.DEFAULT_DIRECTORY}/{account}/{file_name}", "w") as f: # Open json file
            f.write(json.dumps({"creation date": self.__creation_date, "creation time": self.__creation_time, 
                                "mode": self.__mode, "difficulty": self.__difficulty, "num of hints": self.__num_of_hints, 
                                "board size": self.__board_size, "board": self.__board.hash(), 
                                "orig board": self.__orig_board.hash(), "timed": self.__timed, 
                                "time elapsed": self.__time_elapsed}, indent=4)) # Write data to json file
    
    def remove_game_file(self, account): # Remove game file when game is resigned or won
        if self.__file is not None:
            if os.path.exists(path := f"{self.DEFAULT_DIRECTORY}/{account}/{self.__file}"):
                os.remove(path) # Remove file if the file exists

    def get_stats(self, completed):
        return [self.__mode, self.__difficulty, self.__board_size, self.__orig_num_of_hints, self.__num_of_hints, self.__timed, completed, 
                self.__time_elapsed, self.__creation_date, self.__creation_time]
    
    '''Getters'''

    @property
    def difficulty(self): # Gets difficulty (returns str)
        return self.__difficulty
    
    @property
    def orig_num_hints(self): # Gets original number of hints given (returns int)
        return self.__orig_num_of_hints

    @property
    def num_hints_left(self): # Gets number of hints left (returns int)
        return self.__num_of_hints
    
    @property
    def mode(self): # Gets mode (returns str)
        return self.__mode

    @property
    def timed(self): # Gets timed (returns bool)
        return self.__timed
    
    @property
    def time_elapsed(self): # Getstime elapsed (returns str)
        return str(timedelta(seconds=floor(self.__time_elapsed)))
    
    @property
    def board_size(self): # Gets board size (returns int)
        return self.__board_size
    
    @property
    def matrix_size(self): # Gets matrix size (returns tuple)
        return self.__board.matrix_size
    
    @property
    def curr_board(self): # Gets current board 2D array (returns 2D array of square objects)
        return self.__board.board
    
    @property
    def orig_board(self): # Gets original board 2D array (returns 2D array of square objects)
        return self.__orig_board.board
    
    @property
    def solved_board(self): # Gets solved board (returns 2D array of square objects)
        return BoardSolver.solver(deepcopy(self.__orig_board)).board
    
    @property
    def groups(self): # Gets groups (returns dictionary if board is a killer mode board, returns None otherwise)
        if isinstance(self.__board, KillerModeBoard):
            return self.__board.groups
    
    @property
    def group_colours(self): # Gets group colours (returns dictionary if board is a killer mode board, returns None otherwise)
        if isinstance(self.__board, KillerModeBoard):
            return self.__board.group_colours()

    def note_at(self, row, col): # Gets note at square (returns str) : only used for GUI
        return self.__board.note_str(row, col)

    def pieced_note_at(self, row, col, piece): # Gets note at square (returns str) : only usd for TERMINAL
        return self.__board.pieced_note_str(row, col, piece)
    
    '''Other various methods'''

    def inc_time_elapsed(self): # Incerement time elapsed every 0.01 seconds (10 milliseconds)
        self.__time_elapsed += 0.01
    
    def is_complete(self): # Check if board is complete (returns bool)
        return self.__board.num_empty_squares == 0

    def percent_complete(self): # Gets percentage completion for progress bar
        return round(((num_orig_empty := self.__orig_board.num_empty_squares) - self.__board.num_empty_squares)/num_orig_empty * 100, 2)

    def push_action(self, action): # Push action to stack
        self.__action_stack.push(action)

    def pop_action(self): # Pop action from stack
        return self.__action_stack.pop()
    
    def __validate(self, n): # Validate method (for user interaction with game)
        try:
            if (n := int(n)) not in self.__VALID_NUMS:
                raise GameError("Number inputted is not between 1 and 9")
            return n
        except TypeError:
            raise GameError("Number inputted is not an integer")
        except ValueError:
            raise GameError("Number inputted is not an integer")
    
    '''UI Specific Methods to interact with the game/board (with validation)'''

    def put_down_number(self, row, col, num): # Put down number method (takes row, col, num where row, col are in a 1-based system)
        row, col, num = self.__validate(row) - 1, self.__validate(col) - 1, self.__validate(to_num(num))
        if (orig_num := self.__board.get_num_at(row, col)) == 0:
            if self.__board.is_safe(row, col, num):
                self.__board.set_num_at(row, col, num)
            else:
                raise GameError(f"Please enter a number that doesn't exist in the row / column / 3x3 matrix you specified")
        else:
            raise GameError(f"A number already exists at this square")
        self.push_action(SetNumAction(row, col, orig_num, num))
    
    def remove_number(self, row, col): # Remove number method (takes row, col, both are in a 1-based system)
        row, col = self.__validate(row) - 1, self.__validate(col) - 1 # '-1' is used to convert 1-based system to a 0-based system
        if (orig_num := self.__board.get_num_at(row, col)) == 0:
            raise GameError(f"There is no number at this square that you can delete")
        else:
            if self.__orig_board.get_num_at(row, col) != 0:
                raise GameError(f"This square is part of the original board and cannot be deleted")
            else:
                self.__board.set_num_at(row, col, 0)
        self.push_action(SetNumAction(row, col, orig_num, 0))
    
    def edit_note(self, row, col, num): # Edit (toggle) note method (takes row, col, num, where row, col are in a 1-based system)
        row, col, num = self.__validate(row)-1, self.__validate(col)-1, self.__validate(to_num(num)) # '-1' is used to convert 1-based system to a 0-based system
        self.__board.toggle_num_at_note(row, col, num)
        self.push_action(EditNoteAction(row, col, num))
    
    def __get_hint_at(self, row, col): # INTERNAL PRIVATE Get hint at square method (takes row, col where both are in a 0-based system)
        if self.__board.get_num_at(row, col) != 0:
            raise GameError(f"ERROR: Hint is unavailable for this square as it is not empty")
        if self.__num_of_hints == 0:
            raise GameError(f"Not enough hints")
        self.__num_of_hints -= 1
        return [self.__board.is_safe(row, col, num) for num in self.__VALID_NUMS]
    
    def add_hint_to_notes(self, row, col): # EXTERNAL Give hint by adding to notes method (takes row, col where both are in a 1-based system)
        row, col = self.__validate(row)-1, self.__validate(col)-1 # '-1' is used to convert 1-based system to a 0-based system
        orig_note = self.__board.get_note_at(row, col)
        self.__board.set_note_at(row, col, new_note := self.__get_hint_at(row, col))
        self.push_action(SetNoteAction(row, col, orig_note, new_note))
    
    def undo_last_move(self): # Undo method, uses BoardActions imported from board_actions.py
        if (action := self.pop_action()) != -1: # Check if action stack isn't empty
            reverse_action = action.reverse() # Get reverse of that action
            if isinstance(reverse_action, SetNumAction): # Apply the reverse action (for SetNumAction)
                self.__board.set_num_at(reverse_action.row, reverse_action.col, reverse_action.new_num)
            elif isinstance(reverse_action, EditNoteAction): # (for EditNoteAction)
                self.__board.toggle_num_at_note(reverse_action.row, reverse_action.col, reverse_action.num)
            elif isinstance(reverse_action, SetNoteAction): # (for SetNoteAction)
                self.__board.set_note_at(reverse_action.row, reverse_action.col, reverse_action.new_note)
    
    def rating_change(self, rating, won):
        if won:
            return rating_gain(self.__mode, self.__board_size, self.__difficulty, rating, self.__time_elapsed)
        else:
            return -rating_loss(self.__mode, self.__board_size, self.__difficulty, rating)
