from board import *

class Game:
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
    
    def is_complete(self):
        return self.__board.num_empty_squares(self.__board.get_curr_board()) == 0

    def percent_complete(self):
        return round(((num_orig_empty := self.__board.num_empty_squares(self.__board.get_orig_board())) - self.__board.num_empty_squares(self.__board.get_curr_board()))/num_orig_empty * 100, 2)

