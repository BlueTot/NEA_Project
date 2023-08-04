from board import *

class Game:

    DIFFICULTY_NUMS = {1: "Easy", 2: "Medium", 3: "Hard", 4:"Challenge"}
    
    def __init__(self, difficulty):
        self.__difficulty = difficulty
        self.__mode = "Normal"
        self.__board_size = 9
        self.__board = Board(self.__difficulty)
    
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
    def board(self):
        return self.__board
    
    def curr_board(self):
        return self.__board.get_curr_board()
    
    def orig_board(self):
        return self.__board.get_orig_board()
    
    def solved_board(self):
        return self.__board.get_solved_board()
    
    def put_down_number(self, row, col, num):
        self.__board.set_num_at(row, col, num)
    
    def remove_number(self, row, col):
        self.__board.remove_num_at(row, col)
    
    def get_hint_at(self, row, col):
        return self.__board.get_hint_for_sq(row, col)
    
    def is_complete(self):
        return self.__board.num_empty_squares(self.__board.get_curr_board()) == 0

    def percent_complete(self):
        return round(((num_orig_empty := self.__board.num_empty_squares(self.__board.get_orig_board())) - self.__board.num_empty_squares(self.__board.get_curr_board()))/num_orig_empty * 100, 2)
