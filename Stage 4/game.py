from board import *
from stack import Stack
from datetime import datetime
import json
import os

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    DEFAULT_DIRECTORY = "games"
    DEFAULT_DIFFICULTY = "Easy"
    DEFAULT_MODE = "Normal"
    
    def __init__(self, difficulty=DEFAULT_DIFFICULTY):
        self.__difficulty = difficulty
        self.__mode = self.DEFAULT_MODE
        self.__board = Board(self.__difficulty)
        self.__board_state_stack = Stack()
        self.__notes_state_stack = Stack()
        self.__notes = Notes()
        self.__file = None
    
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
        return self.__notes.note_str(row, col)

    def push_state(self):
        self.__board_state_stack.push(self.__board.hash())
        self.__notes_state_stack.push(self.__notes.hash())

    def pop_state(self):
        return self.__board_state_stack.pop(), self.__notes_state_stack.pop()
    
    def curr_state(self):
        board_state = state if (state := self.__board_state_stack.peek()) != -1 else self.__board.orig_hash()
        notes_state = state if (state := self.__notes_state_stack.peek()) != -1 else self.__notes.orig_hash()
        return board_state, notes_state

    def load_state(self, states):
        self.__board.load_board(states[0])
        self.__notes.load_notes(states[1])
    
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
        self.__notes.toggle_number_at_note(row, col, num)
        self.push_state()
    
    def add_hint_to_notes(self, row, col, nums):
        curr_note = self.__notes.note_at(row, col)
        for num in range(1, 10):
            if (num in curr_note) != (num in nums):
                self.__notes.toggle_number_at_note(row, col, num)
        self.push_state()
    
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
        self.__difficulty = data["difficulty"]
        self.__board.load_board(data["board"])
        self.__board.set_orig_board(data["orig board"])
        self.__notes.load_notes(data["notes"])
    
    def save_game(self):
        file_name = f"singleplayer_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.json" if self.__file is None else self.__file
        with open(f"{self.DEFAULT_DIRECTORY}/{file_name}", "w") as f:
            f.write(json.dumps({"creation date": str(datetime.now().date()), "creation time": str(datetime.now().time()), 
                                "mode": self.__mode, "difficulty": self.__difficulty, "board": self.__board.hash(), 
                                "orig board": self.__board.orig_hash(), "notes": self.__notes.hash()}, indent=4))
    
    def remove_game_file(self):
        if self.__file is not None:
            if os.path.exists(path := f"{self.DEFAULT_DIRECTORY}/{self.__file}"):
                os.remove(path)
