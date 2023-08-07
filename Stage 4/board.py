from copy import deepcopy
from random import randint
from abc import ABC

class BoardError(Exception):
    pass

class BoardSolver:

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

    @staticmethod
    def is_safe(grid, row, col, num):
        return (not BoardSolver.__in_row(grid, row, num)) and (not BoardSolver.__in_col(grid, col, num)) and (not BoardSolver.__in_3x3_matrix(grid, row, col, num))

    @staticmethod
    def solvable(board, row=0, col=0):

        if col == 9 and row == 8:
            return True
        
        if col == 9:
            col = 0
            row += 1
        
        if board[row][col] > 0:
            return BoardSolver.solvable(board, row, col+1)
        for num in range(1, 10):
            if BoardSolver.is_safe(board, row, col, num):
                board[row][col] = num
                if BoardSolver.solvable(board, row, col+1):
                    return True
            board[row][col] = 0

        return False
    
    @staticmethod
    def solver(board):
        return new_board if BoardSolver.solvable(new_board := deepcopy(board)) else -1

class BoardGenerator:
    @staticmethod
    def __fill_matrix_randomly(grid, start, end):
        for row in range(start, end+1):
            for col in range(start, end+1):
                while not BoardSolver.is_safe(grid, row, col, num := randint(1, 9)):
                    pass
                grid[row][col] = num
        return grid
    
    @staticmethod
    def __get_random_filled_board():
        board = [[0 for _ in range(9)] for _ in range(9)]
        board = BoardGenerator.__fill_matrix_randomly(board, 0, 2)
        board = BoardGenerator.__fill_matrix_randomly(board, 3, 5)
        board = BoardGenerator.__fill_matrix_randomly(board, 6, 8)
        return BoardSolver.solver(board)

    @staticmethod
    def new_board(difficulty):
        board = BoardGenerator.__get_random_filled_board()
        for _ in range(Board.NUM_NUMS_TO_REMOVE[difficulty]):
            while board[row := randint(0, 8)][col := randint(0, 8)] == 0:
                pass
            board[row][col] = 0
        return board

class Grid(ABC):

    VALID_NUMS = [i for i in range(1, 10)]

    def __init__(self):
        pass

    def _validate(self, n):
        try:
            if (n := int(n)) not in self.VALID_NUMS:
                raise BoardError("Number inputted is not between 1 and 9")
            return n
        except TypeError:
            raise BoardError("Number inputted is not an integer")
        except ValueError:
            raise BoardError("Number inputted is not an integer")
        
class Board(Grid):

    NUM_NUMS_TO_REMOVE = {"Easy": 36, "Medium": 45, "Hard": 54, "Challenge": 60}

    def __init__(self, difficulty):
        super().__init__()
        self.__difficulty = difficulty
        self.__board = BoardGenerator.new_board(self.__difficulty)
        self.__orig_board = deepcopy(self.__board)
    
    def load_board(self, hash):
        for idx, num in enumerate(hash):
            self.__board[idx // 9][idx % 9] = int(num)
    
    def get_curr_board(self):
        return self.__board
    
    def get_orig_board(self):
        return self.__orig_board
    
    def get_difficulty(self):
        return self.__difficulty
    
    @staticmethod
    def __hash(board):
        return "".join(["".join(list(map(str, row))) for row in board])
    
    def hash(self):
        return self.__hash(self.__board)
    
    def orig_hash(self):
        return self.__hash(self.__orig_board)

    def set_num_at(self, row, col, num):
        row, col, num = self._validate(row) - 1, self._validate(col) - 1, self._validate(num)
        if self.__board[row][col] == 0:
            if BoardSolver.is_safe(self.__board, row, col, num):
                self.__board[row][col] = num
            else:
                raise BoardError(f"Please enter a number that doesn't exist in the row / column / 3x3 matrix you specified")
        else:
            raise BoardError(f"A number already exists at this square")
    
    def remove_num_at(self, row, col):
        row, col = self._validate(row) - 1, self._validate(col) - 1
        if self.__board[row][col] == 0:
            raise BoardError(f"There is no number at this square that you can delete")
        else:
            if self.__orig_board[row][col] != 0:
                raise BoardError(f"This square is part of the original board and cannot be deleted")
            else:
                self.__board[row][col] = 0
    
    def get_hint_for_sq(self, row, col):
        row, col = self._validate(row) - 1, self._validate(col) - 1
        if self.__board[row][col] != 0:
            raise BoardError(f"ERROR: Hint is unavailable for this square as it is not empty")
        return [num for num in range(1, 10) if BoardSolver.is_safe(self.__board, row, col, num)]
    
    def num_empty_squares(self, board):
        return self.__hash(board).count("0")

    def get_solved_board(self):
        return BoardSolver.solver(self.__orig_board)
        
class Notes(Grid):
    def __init__(self):
        super().__init__()
        self.__notes = [[set() for _ in range(9)] for _ in range(9)]

    def note_str(self, row, col):
        return "\n".join([" " + " ".join([str(j+1) if j+1 in self.__notes[row][col] else "  " for j in range(i*3, (i+1)*3)]) for i in range(3)])
    
    def toggle_number_at_note(self, row, col, num):
        row, col, num = self._validate(row)-1, self._validate(col)-1, self._validate(num)
        if num in self.__notes[row][col]:
            self.__notes[row][col].remove(num)
        else:
            self.__notes[row][col].add(num)

