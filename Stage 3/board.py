from copy import deepcopy
from random import randint

class InvalidNumberError(Exception):
    pass

class SquareAlreadyFilledError(Exception):
    pass

class SquareAlreadyEmptyError(Exception):
    pass

class SquareCannotBeDeletedError(Exception):
    pass

class Board:

    valid_nums = [str(i) for i in range(1, 10)]

    num_nums_to_remove = {"easy": 36, "medium": 45, "hard": 54, "challenge": 60}

    def __init__(self, difficulty):
        self.__difficulty = difficulty
        self.__board = self.generate_new_board(self.__difficulty)
        self.__orig_board = deepcopy(self.__board)

    def __fill_matrix_randomly(self, grid, start, end):
        for row in range(start, end+1):
            for col in range(start, end+1):
                while not self.__is_safe(grid, row, col, num := randint(1, 9)):
                    pass
                grid[row][col] = num
        return grid
    
    def get_random_filled_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        board = self.__fill_matrix_randomly(board, 0, 2)
        board = self.__fill_matrix_randomly(board, 3, 5)
        board = self.__fill_matrix_randomly(board, 6, 8)
        return self.get_solved_board(board)

    def generate_new_board(self, difficulty):
        board = self.get_random_filled_board()
        for _ in range(Board.num_nums_to_remove[difficulty]):
            while board[row := randint(0, 8)][col := randint(0, 8)] == 0:
                pass
            board[row][col] = 0
        return board
    
    def set_num_at(self, row, col, num):
        row -= 1
        col -= 1
        if self.__board[row][col] == 0:
            if self.__is_safe(self.__board, row, col, num):
                self.__board[row][col] = num
            else:
                raise InvalidNumberError
        else:
            raise SquareAlreadyFilledError
    
    def remove_num_at(self, row, col):
        row -= 1
        col -= 1
        if self.__board[row][col] == 0:
            raise SquareAlreadyEmptyError
        else:
            if self.__orig_board[row][col] != 0:
                raise SquareCannotBeDeletedError
            else:
                self.__board[row][col] = 0
    
    def get_hint_for_sq(self, row, col):
        row -= 1
        col -= 1
        if self.__board[row][col] != 0:
            raise SquareAlreadyFilledError
        return [num for num in range(1, 10) if self.__is_safe(self.__board, row, col, num)]
    
    def get_curr_board(self):
        return self.__board
    
    def get_orig_board(self):
        return self.__orig_board
    
    def get_difficulty(self):
        return self.__difficulty

    @staticmethod
    def num_empty_squares(board):
        num_empty = 0
        for row in board:
            for num in row:
                if num == 0:
                    num_empty += 1
        return num_empty

    @staticmethod
    def __in_row(grid, row, num):
        return num in grid[row]

    @staticmethod
    def __in_col(grid, col, num):
        return num in [row[col] for row in grid]

    @staticmethod
    def __in_3x3_matrix(grid, row, col, num):
        box_row, box_col = row // 3, col // 3
        box = []
        for row in range(3*box_row, 3*(box_row + 1)):
            for col in range(3*box_col, 3*(box_col+1)):
                box.append(grid[row][col])
        return num in box

    def __is_safe(self, grid, row, col, num):
        return (not self.__in_row(grid, row, num)) and (not self.__in_col(grid, col, num)) and (not self.__in_3x3_matrix(grid, row, col, num))

    def __solve_sudoku(self, board, row=0, col=0):

        if col == 9 and row == 8:
            return True
        
        if col == 9:
            col = 0
            row += 1
        
        if board[row][col] > 0:
            return self.__solve_sudoku(board, row, col+1)
        for num in range(1, 10):
            if self.__is_safe(board, row, col, num):
                board[row][col] = num
                if self.__solve_sudoku(board, row, col+1):
                    return True
            board[row][col] = 0

        return False
    
    def get_solved_board(self, *args):
        if len(args) == 0:
            new_board = deepcopy(self.__orig_board)
        else:
            new_board = deepcopy(args[0])
        if self.__solve_sudoku(new_board):
            return new_board
        else:
            return -1
