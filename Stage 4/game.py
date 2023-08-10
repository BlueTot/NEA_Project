from board import *
from stack import Stack

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    
    def __init__(self, difficulty):
        self.__difficulty = difficulty
        self.__mode = "Normal"
        self.__board_size = 9
        self.__board = Board(self.__difficulty)
        self.__board_state_stack = Stack()
        self.__notes_state_stack = Stack()
        self.__notes = Notes()
    
    @property
    def difficulty(self):
        return self.__difficulty
    
    @property
    def mode(self):
        return self.__mode
    
    @property
    def board_size(self):
        return self.__board_size
    
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
