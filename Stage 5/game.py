from board import *
from stack import Stack
from datetime import datetime
import json
import os

class GameError(Exception):
    pass

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    DEFAULT_DIRECTORY = "games"
    DEFAULT_DIFFICULTY = "Easy"
    DEFAULT_MODE = "Normal"
    
    def __init__(self, difficulty=DEFAULT_DIFFICULTY):
        self.__difficulty = difficulty
        self.__mode = self.DEFAULT_MODE
        self.__board = Board(self.__difficulty)
        self.__state_stack = Stack()
        self.__file = None
        self.__last_saved_state = self.__board.orig_hash()
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
        return self.__board.get_curr_board()
    
    @property
    def orig_board(self):
        return self.__board.get_orig_board()

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
        self.__board.load_board(state)
    
    @property
    def solved_board(self):
        return self.__board.get_solved_board()

    def put_down_number(self, row, col, num):
        self.__board.set_num_at(row, col, num)
        self.push_state()
    
    def remove_number(self, row, col):
        self.__board.remove_num_at(row, col)
        self.push_state()
    
    def get_hint_at(self, row, col):
        return self.__board.get_hint_for_sq(row, col)
    
    def edit_note(self, row, col, num):
        self.__board.toggle_number_at_note(row, col, num)
        self.push_state()
    
    def add_hint_to_notes(self, row, col, nums):
        curr_note = self.__board.note_at(row, col)
        for num in range(1, 10):
            if curr_note[num-1] != (num in nums):
                self.__board.toggle_number_at_note(row, col, num)
        self.push_state()
    
    def undo_last_move(self):
        self.pop_state()
        self.load_state(self.curr_state())
    
    def is_complete(self):
        return self.__board.num_empty_squares(self.__board.get_curr_board()) == 0

    def percent_complete(self):
        return round(((num_orig_empty := self.__board.num_empty_squares(self.__board.get_orig_board())) - self.__board.num_empty_squares(self.__board.get_curr_board()))/num_orig_empty * 100, 2)

    @staticmethod
    def get_stats_from(file):
        with open(f"{Game.DEFAULT_DIRECTORY}/{file}") as f:
            return json.load(f)

    def load_game(self, file):
        data = self.get_stats_from(file)
        self.__file = file
        self.__last_saved_state = data["board"]
        self.__difficulty = data["difficulty"]
        self.__board.load_board(data["board"])
        self.__board.set_orig_board(data["orig board"])
        self.__creation_date = data["creation date"]
        self.__creation_time = data["creation time"]
    
    def save_game(self):
        file_name = f"singleplayer_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.json" if self.__file is None else self.__file
        with open(f"{self.DEFAULT_DIRECTORY}/{file_name}", "w") as f:
            f.write(json.dumps({"creation date": self.__creation_date, "creation time": self.__creation_time, 
                                "mode": self.__mode, "difficulty": self.__difficulty, "board": self.__board.hash(), 
                                "orig board": self.__board.orig_hash()}, indent=4))
    
    def remove_game_file(self):
        if self.__file is not None:
            if os.path.exists(path := f"{self.DEFAULT_DIRECTORY}/{self.__file}"):
                os.remove(path)
