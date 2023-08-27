from board import BoardGenerator, BoardSolver
from stack import Stack
from datetime import datetime
import json
import os
from copy import deepcopy

class GameError(Exception):
    pass

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    DEFAULT_DIRECTORY = "games"
    DEFAULT_DIFFICULTY = "Easy"
    DEFAULT_MODE = "Normal"
    VALID_NUMS = [i for i in range(1, 10)]
    
    def __init__(self, difficulty=DEFAULT_DIFFICULTY):
        self.__difficulty = difficulty
        self.__mode = self.DEFAULT_MODE
        self.__board = BoardGenerator.new_board(self.__difficulty)
        self.__orig_board = deepcopy(self.__board)
        self.__state_stack = Stack()
        self.__file = None
        self.__last_saved_state = self.__orig_board.hash()
        self.__creation_date = str(datetime.now().date())
        self.__creation_time = str(datetime.now().time())
    
    @property
    def difficulty(self):
        return self.__difficulty
    
    @property
    def mode(self):
        return self.__mode
    
    @property
    def curr_board(self):
        return self.__board.board
    
    @property
    def orig_board(self):
        return self.__orig_board.board

    def note_at(self, row, col):
        return self.__board.note_str(row, col)

    def pieced_note_at(self, row, col, piece):
        return self.__board.pieced_note_str(row, col, piece)

    def push_state(self):
        self.__state_stack.push(self.__board.hash())

    def pop_state(self):
        return self.__state_stack.pop()
    
    def curr_state(self):
        return state if (state := self.__state_stack.peek()) != -1 else self.__last_saved_state

    def load_state(self, state):
        self.__board.load(state)
    
    @property
    def solved_board(self):
        return BoardSolver.solver(self.__orig_board).board

    def __validate(self, n):
        try:
            if (n := int(n)) not in self.VALID_NUMS:
                raise GameError("Number inputted is not between 1 and 9")
            return n
        except TypeError:
            raise GameError("Number inputted is not an integer")
        except ValueError:
            raise GameError("Number inputted is not an integer")

    def put_down_number(self, row, col, num):
        row, col, num = self.__validate(row) - 1, self.__validate(col) - 1, self.__validate(num)
        if self.__board.get_num_at(row, col) == 0:
            if self.__board.is_safe(row, col, num):
                self.__board.set_num_at(row, col, num)
            else:
                raise GameError(f"Please enter a number that doesn't exist in the row / column / 3x3 matrix you specified")
        else:
            raise GameError(f"A number already exists at this square")
        self.push_state()
    
    def remove_number(self, row, col):
        row, col = self.__validate(row) - 1, self.__validate(col) - 1
        if self.__board.get_num_at(row, col) == 0:
            raise GameError(f"There is no number at this square that you can delete")
        else:
            if self.__orig_board.get_num_at(row, col) != 0:
                raise GameError(f"This square is part of the original board and cannot be deleted")
            else:
                self.__board.set_num_at(row, col, 0)
        self.push_state()
    
    def get_hint_at(self, row, col):
        row, col = self.__validate(row) - 1, self.__validate(col) - 1
        if self.__board.get_num_at(row, col) != 0:
            raise GameError(f"ERROR: Hint is unavailable for this square as it is not empty")
        return [num for num in range(1, 10) if self.__board.is_safe(row, col, num)]
    
    def edit_note(self, row, col, num):
        row, col, num = self.__validate(row)-1, self.__validate(col)-1, self.__validate(num)
        self.__board.toggle_num_at_note(row, col, num)
        self.push_state()
    
    def add_hint_to_notes(self, row, col, nums):
        row, col = self.__validate(row)-1, self.__validate(col)-1
        curr_note = self.__board.get_note_at(row, col)
        for num in range(1, 10):
            if curr_note[num-1] != (num in nums):
                self.__board.toggle_num_at_note(row, col, num)
        self.push_state()
    
    def undo_last_move(self):
        self.pop_state()
        self.load_state(self.curr_state())
    
    def is_complete(self):
        return self.__board.num_empty_squares() == 0

    def percent_complete(self):
        return round(((num_orig_empty := self.__orig_board.num_empty_squares()) - self.__board.num_empty_squares())/num_orig_empty * 100, 2)

    @staticmethod
    def get_stats_from(file):
        with open(f"{Game.DEFAULT_DIRECTORY}/{file}") as f:
            return json.load(f)

    def load_game(self, file):
        data = self.get_stats_from(file)
        self.__file = file
        self.__last_saved_state = data["board"]
        self.__difficulty = data["difficulty"]
        self.__board.load(data["board"])
        self.__orig_board.load(data["orig board"])
        self.__creation_date = data["creation date"]
        self.__creation_time = data["creation time"]
    
    def save_game(self):
        file_name = f"singleplayer_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.json" if self.__file is None else self.__file
        with open(f"{self.DEFAULT_DIRECTORY}/{file_name}", "w") as f:
            f.write(json.dumps({"creation date": self.__creation_date, "creation time": self.__creation_time, 
                                "mode": self.__mode, "difficulty": self.__difficulty, "board": self.__board.hash(), 
                                "orig board": self.__orig_board.hash()}, indent=4))
    
    def remove_game_file(self):
        if self.__file is not None:
            if os.path.exists(path := f"{self.DEFAULT_DIRECTORY}/{self.__file}"):
                os.remove(path)
