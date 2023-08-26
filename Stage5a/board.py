from copy import deepcopy
from random import randint

class BoardSolver:

    @staticmethod
    def solvable(board, row=0, col=0):

        if col == 9 and row == 8:
            return True
        
        if col == 9:
            col = 0
            row += 1
        
        if board.get_num_at(row, col) > 0:
            return BoardSolver.solvable(board, row, col+1)
        for num in range(1, 10):
            if board.is_safe(row, col, num):
                board.set_num_at(row, col, num)
                if BoardSolver.solvable(board, row, col+1):
                    return True
            board.set_num_at(row, col, 0)

        return False
    
    @staticmethod
    def solver(board):
        return new_board if BoardSolver.solvable(new_board := deepcopy(board)) else -1

class BoardGenerator:

    @staticmethod
    def __fill_matrix_randomly(board, start, end):
        for row in range(start, end+1):
            for col in range(start, end+1):
                while not board.is_safe(row, col, num := randint(1, 9)):
                    pass
                board.set_num_at(row, col, num)
        return board
    
    @staticmethod
    def __get_random_filled_board():
        board = NormalModeBoard()
        board = BoardGenerator.__fill_matrix_randomly(board, 0, 2)
        board = BoardGenerator.__fill_matrix_randomly(board, 3, 5)
        board = BoardGenerator.__fill_matrix_randomly(board, 6, 8)
        return BoardSolver.solver(board)

    @staticmethod
    def new_board(difficulty):
        board = BoardGenerator.__get_random_filled_board()
        for _ in range(Board.NUM_NUMS_TO_REMOVE[difficulty]):
            while board.get_num_at(row := randint(0, 8), col := randint(0, 8)) == 0:
                pass
            board.set_num_at(row, col, 0)
        return board

class Square:
    def __init__(self):
        self.__num = 0
        self.__note = [False for _ in range(9)]
    
    @property
    def num(self):
        return self.__num
    
    @property
    def note(self):
        return self.__note
    
    def set_num(self, num):
        self.__num = num

    def edit_note(self, num):
        self.__note[num - 1] = not self.__note[num - 1]
    
    def hash(self):
        return f"{self.__num},{''.join([str(num+1) for num in range(len(self.__note)) if self.__note[num]])}"
    
    def load(self, hash):
        num, note = hash.split(",")
        self.__num = int(num)
        self.__note = [str(num+1) in note for num in range(9)]

    def note_str(self):
        return "\n".join([" " + " ".join([str(j+1) if self.__note[j] else "  " for j in range(i*3, (i+1)*3)]) for i in range(3)])

    def pieced_note_str(self, piece):
        return "".join([str(i+1) if self.__note[i] else " " for i in range((piece-1)*3, piece*3)])
    
    def __repr__(self):
        return str(self.__num)

class Board:

    NUM_NUMS_TO_REMOVE = {"Easy": 36, "Medium": 45, "Hard": 54, "Challenge": 60}

    def __init__(self):
        self._board = [[Square() for _ in range(9)] for _ in range(9)]
        self._row_digits = [0 for _ in range(9)]
        self._col_digits = [0 for _ in range(9)]
        self._matrix_digits = [0 for _ in range(9)]
    
    @property
    def row_digits(self):
        return [bin(n) for n in self._row_digits]
    
    @property
    def col_digits(self):
        return [bin(n) for n in self._col_digits]
    
    @property
    def matrix_digits(self):
        return [bin(n) for n in self._matrix_digits]
    
    @staticmethod
    def _bwn(num):
        return num ^ ((2**9) - 1)
    
    @staticmethod
    def _bin(num):
        return 2 ** (num - 1)
    
    @staticmethod
    def _matrix_num(row, col):
        return 3 * (row // 3) + col // 3
    
    @property
    def board(self):
        return self._board
    
    def get_num_at(self, row, col):
        return self._board[row][col].num

    def get_note_at(self, row, col):
        return self._board[row][col].note
    
    def set_num_at(self, row, col, num):
        if num > 0:
            self._row_digits[row] += (bin := self._bin(num))
            self._col_digits[col] += bin
            self._matrix_digits[self._matrix_num(row, col)] += bin
        elif (orig_num := self.get_num_at(row, col)) != 0:
            self._row_digits[row] -= (bin := self._bin(orig_num))
            self._col_digits[col] -= bin
            self._matrix_digits[self._matrix_num(row, col)] -= bin
        self._board[row][col].set_num(num)
    
    def toggle_num_at_note(self, row, col, num):
        self._board[row][col].edit_note(num)
    
    def load(self, hash):
        for idx, sq_hash in enumerate(hash.split(";")):
            self._board[idx // 9][idx % 9].load(sq_hash)
    
    def hash(self):
        return ";".join([";".join([sq.hash() for sq in row]) for row in self._board])
    
    def num_empty_squares(self):
        return sum([sum([1 for sq in row if sq.num == 0]) for row in self._board])

    def note_str(self, row, col):
        return self._board[row][col].note_str()
    
    def pieced_note_str(self, row, col, piece):
        return self._board[row][col].pieced_note_str(piece)

    def get_solved_board(self):
        return BoardSolver.solver(self.__orig_board)

class NormalModeBoard(Board):
    def __init__(self):
        super().__init__()

    def __not_in_row(self, row, num):
        return self._bwn(self._row_digits[row]) & self._bin(num)

    def __not_in_col(self, col, num):
        return self._bwn(self._col_digits[col]) & self._bin(num)

    def __not_in_3x3_matrix(self, row, col, num):
        return self._bwn(self._matrix_digits[self._matrix_num(row, col)]) & self._bin(num)

    def is_safe(self, row, col, num):
        return self.__not_in_row(row, num) and self.__not_in_col(col, num) and self.__not_in_3x3_matrix(row, col, num)
    