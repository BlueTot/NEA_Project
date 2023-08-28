from board import *
from stack import Stack
from datetime import datetime, timedelta
import json
import os
from copy import deepcopy
from math import floor

class GameError(Exception):
    pass

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    DEFAULT_DIRECTORY = "games"
    DEFAULT_DIFFICULTY = "Easy"
    DEFAULT_MODE = "Normal"
    VALID_NUMS = [i for i in range(1, 10)]
    
    def __init__(self):
        self.__difficulty = None
        self.__mode = self.DEFAULT_MODE
        self.__board = NormalModeBoard()
        self.__orig_board = deepcopy(self.__board)
        self.__action_stack = Stack()
        self.__file = None
        self.__creation_date = str(datetime.now().date())
        self.__creation_time = str(datetime.now().time())
        self.__timed = None
        self.__time_elapsed = None
    
    def generate(self, difficulty, timed):
        self.__difficulty = difficulty
        self.__board = BoardGenerator.new_board(self.__difficulty)
        self.__orig_board = deepcopy(self.__board)
        self.__timed = timed
        self.__time_elapsed = 0 if self.__timed else None
    
    @staticmethod
    def get_stats_from(file):
        with open(f"{Game.DEFAULT_DIRECTORY}/{file}") as f:
            return json.load(f)

    def load_game(self, file):
        data = self.get_stats_from(file)
        self.__file = file
        self.__difficulty = data["difficulty"]
        self.__board.load(data["board"])
        self.__orig_board.load(data["orig board"])
        self.__creation_date = data["creation date"]
        self.__creation_time = data["creation time"]
        self.__timed = data["timed"]
        self.__time_elapsed = data["time elapsed"]
    
    def save_game(self):
        file_name = f"singleplayer_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.json" if self.__file is None else self.__file
        with open(f"{self.DEFAULT_DIRECTORY}/{file_name}", "w") as f:
            f.write(json.dumps({"creation date": self.__creation_date, "creation time": self.__creation_time, 
                                "mode": self.__mode, "difficulty": self.__difficulty, "board": self.__board.hash(), 
                                "orig board": self.__orig_board.hash(), "timed": self.__timed,
                                "time elapsed": self.__time_elapsed}, indent=4))
    
    def remove_game_file(self):
        if self.__file is not None:
            if os.path.exists(path := f"{self.DEFAULT_DIRECTORY}/{self.__file}"):
                os.remove(path)
    
    @property
    def difficulty(self):
        return self.__difficulty
    
    @property
    def mode(self):
        return self.__mode

    @property
    def timed(self):
        return self.__timed
    
    @property
    def time_elapsed(self):
        return str(timedelta(seconds=floor(self.__time_elapsed)))
    
    def inc_time_elapsed(self):
        self.__time_elapsed += 0.01
    
    @property
    def curr_board(self):
        return self.__board.board
    
    @property
    def orig_board(self):
        return self.__orig_board.board
    
    @property
    def solved_board(self):
        return BoardSolver.solver(self.__orig_board).board

    def note_at(self, row, col):
        return self.__board.note_str(row, col)

    def pieced_note_at(self, row, col, piece):
        return self.__board.pieced_note_str(row, col, piece)
    
    def is_complete(self):
        return self.__board.num_empty_squares() == 0

    def percent_complete(self):
        return round(((num_orig_empty := self.__orig_board.num_empty_squares()) - self.__board.num_empty_squares())/num_orig_empty * 100, 2)

    def push_action(self, action):
        self.__action_stack.push(action)

    def pop_action(self):
        return self.__action_stack.pop()

    def load_state(self, state):
        self.__board.load(state)
    
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
        if (orig_num := self.__board.get_num_at(row, col)) == 0:
            if self.__board.is_safe(row, col, num):
                self.__board.set_num_at(row, col, num)
            else:
                raise GameError(f"Please enter a number that doesn't exist in the row / column / 3x3 matrix you specified")
        else:
            raise GameError(f"A number already exists at this square")
        self.push_action(SetNumAction(row, col, orig_num, num))
    
    def remove_number(self, row, col):
        row, col = self.__validate(row) - 1, self.__validate(col) - 1
        if (orig_num := self.__board.get_num_at(row, col)) == 0:
            raise GameError(f"There is no number at this square that you can delete")
        else:
            if self.__orig_board.get_num_at(row, col) != 0:
                raise GameError(f"This square is part of the original board and cannot be deleted")
            else:
                self.__board.set_num_at(row, col, 0)
        self.push_action(SetNumAction(row, col, orig_num, 0))
    
    def edit_note(self, row, col, num):
        row, col, num = self.__validate(row)-1, self.__validate(col)-1, self.__validate(num)
        self.__board.toggle_num_at_note(row, col, num)
        self.push_action(EditNoteAction(row, col, num))
    
    def __get_hint_at(self, row, col):
        if self.__board.get_num_at(row, col) != 0:
            raise GameError(f"ERROR: Hint is unavailable for this square as it is not empty")
        return [self.__board.is_safe(row, col, num) for num in range(1, 10)]
    
    def add_hint_to_notes(self, row, col):
        row, col = self.__validate(row)-1, self.__validate(col)-1
        orig_note = self.__board.get_note_at(row, col)
        self.__board.set_note_at(row, col, new_note := self.__get_hint_at(row, col))
        self.push_action(SetNoteAction(row, col, orig_note, new_note))
    
    def undo_last_move(self):
        if (action := self.pop_action()) != -1:
            reverse_action = action.reverse()
            if isinstance(reverse_action, SetNumAction):
                self.__board.set_num_at(reverse_action.row, reverse_action.col, reverse_action.new_num)
            elif isinstance(reverse_action, EditNoteAction):
                self.__board.toggle_num_at_note(reverse_action.row, reverse_action.col, reverse_action.num)
            elif isinstance(reverse_action, SetNoteAction):
                self.__board.set_note_at(reverse_action.row, reverse_action.col, reverse_action.new_note)
