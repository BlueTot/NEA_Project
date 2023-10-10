from copy import deepcopy
from random import randint, shuffle, choice
from itertools import product
from abc import ABC
import dlx

class BoardUnsolvableError(Exception):
    pass

def to_letter(num):
    return str(num) if 0 <= num <= 9 else chr(num-10+65)

def to_num(letter):
    return int(letter) if letter.isdigit() else ord(letter) - 65 + 10

def to_matrix_size(board_size):
    for factor in range(int(board_size ** 0.5) + 1, 0, -1):
        if board_size % factor == 0:
            return tuple(sorted((factor, board_size // factor)))

class BoardSolver:

    @staticmethod
    def solvable(board, row=0, col=0):

        if col == board.board_size and row == board.board_size - 1:
            return True
        
        if col == board.board_size:
            col = 0
            row += 1
        
        if board.get_num_at(row, col) > 0:
            return BoardSolver.solvable(board, row, col+1)
        
        nums_to_try = list(range(1, board.board_size + 1))
        shuffle(nums_to_try)

        for num in nums_to_try:
            if board.is_safe(row, col, num):
                board.set_num_at(row, col, num)
                if BoardSolver.solvable(board, row, col+1):
                    return True
            board.set_num_at(row, col, 0)

        return False
    
    @staticmethod
    def solver(board):
        # if not BoardSolver.solvable(new_board := deepcopy(board)):
        #     raise BoardUnsolvableError
        # return new_board
        for sol in dlx.solve_sudoku(board.matrix_size, board.board_as_2darr):
            board.load_from_2darr(sol)
            return board
        raise BoardUnsolvableError

    @staticmethod
    def num_solutions(board, row=0, col=0, num_sols=0):
        if col == board.board_size and row == board.board_size - 1:
            return num_sols + 1
        
        if col == board.board_size:
            col = 0
            row += 1
        
        if board.get_num_at(row, col) > 0:
            return BoardSolver.num_solutions(board, row, col+1, num_sols)
        
        for num in range(1, board.board_size + 1):
            if board.is_safe(row, col, num):
                board.set_num_at(row, col, num)
                if (num_sols := BoardSolver.num_solutions(board, row, col+1, num_sols)) > 1:
                    break 
            board.set_num_at(row, col, 0)
              
        return num_sols
    
    def is_unique(board):
        if isinstance(board, NormalModeBoard):
            return len([sol for sol in dlx.solve_sudoku(board.matrix_size, board.board_as_2darr)]) == 1
        return BoardSolver.num_solutions(board) == 1
        

class BoardGenerator:

    NUM_GIVENS = {4: {"Easy": 8, "Medium": 6, "Hard": 5, "Challenge": 4},
                  6: {"Easy": 17, "Medium": 14, "Hard": 11, "Challenge": 10},
                  9: {"Easy": 38, "Medium": 31, "Hard": 25, "Challenge": 22},
                  12: {"Easy": 68, "Medium": 55, "Hard": 44, "Challenge": 39},
                  16: {"Easy": 120, "Medium": 98, "Hard": 79, "Challenge": 70}
    }
    
    @staticmethod
    def __get_random_filled_board(board_size):
        board = NormalModeBoard(board_size)
        return BoardSolver.solver(board)

    @staticmethod
    def __set_groups(board):

        available_squares = list(product(range(0, board.board_size), repeat=2))

        while available_squares:

            base = choice(available_squares)
            available_squares.remove(base)
            board.create_group(base, board.get_num_at(base[0], base[1]))
            num_squares = 0
            curr_sq = base

            while randint(0, num_squares) == 0:
                adjacent_squares = board.adjacent_non_grouped_cells(curr_sq[0], curr_sq[1])
                if not adjacent_squares:
                    break
                adj_sq = choice(adjacent_squares)
                available_squares.remove(adj_sq)
                board.add_to_group(base, adj_sq, board.get_num_at(adj_sq[0], adj_sq[1]))
                curr_sq = adj_sq
                num_squares += 1
        
        return board
    
    @staticmethod
    def get_random_filled_killer_board(board_size):
        board = KillerModeBoard(board_size)
        board = BoardSolver.solver(board)
        board = BoardGenerator.__set_groups(board)
        return board

    @staticmethod
    def new_board(mode, difficulty, board_size):
        while True:
            try:
                board = BoardGenerator.__get_random_filled_board(board_size) if mode == "Normal" else BoardGenerator.get_random_filled_killer_board(board_size)
                num_remaining = board_size ** 2
                tries = set()
                while num_remaining > BoardGenerator.NUM_GIVENS[board_size][difficulty]:
                    while board.get_num_at(row := randint(0, board_size - 1), col := randint(0, board_size - 1)) == 0:
                        pass
                    orig_num = board.get_num_at(row, col)
                    board.set_num_at(row, col, 0)
                    if not BoardSolver.is_unique(deepcopy(board)):
                        board.set_num_at(row, col, orig_num)
                        tries.add((row, col))
                        if len(tries) == num_remaining:
                            print("fail exit at", num_remaining, "remaining")
                            return board
                    else:
                        num_remaining -= 1
                        tries = set()
                    print(num_remaining, len(tries))
                return board
            except BoardUnsolvableError:
                pass

class Square:
    def __init__(self, board_size, matrix_size):
        self.__BOARD_SIZE = board_size
        self.__MATRIX_SIZE = matrix_size
        self.__num = 0
        self.__note = [False for _ in range(self.__BOARD_SIZE)]
    
    @property
    def num(self):
        return self.__num
    
    @property
    def note(self):
        return self.__note
    
    def set_num(self, num):
        self.__num = num
    
    def set_note(self, note):
        self.__note = note

    def edit_note(self, num):
        self.__note[num - 1] = not self.__note[num - 1]
    
    def hash(self):
        return f"{self.__num},{''.join([str(num+1) for num in range(len(self.__note)) if self.__note[num]])}"
    
    def load(self, hash):
        num, note = hash.split(",")
        self.__num = int(num)
        self.__note = [str(num+1) in note for num in range(self.__BOARD_SIZE)]

    def note_str(self):
        return "\n".join([" " + " ".join([to_letter(j+1) if self.__note[j] else " " for j in range(i*self.__MATRIX_SIZE[1], (i+1)*self.__MATRIX_SIZE[1])]) for i in range(self.__MATRIX_SIZE[0])])

    def pieced_note_str(self, piece):
        return "".join([to_letter(i+1) if self.__note[i] else " " for i in range((piece-1)*self.__MATRIX_SIZE[0], piece*self.__MATRIX_SIZE[0])])
    
    def __repr__(self):
        return str(self.__num)
    
class BoardAction(ABC):
    def __init__(self, row, col):
        self._row = row
        self._col = col
    
    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    def reverse(self):
        raise NotImplementedError

class SetNumAction(BoardAction):
    def __init__(self, row, col, orig_num, new_num):
        super().__init__(row, col)
        self._orig_num = orig_num
        self._new_num = new_num
    
    @property
    def orig_num(self):
        return self._orig_num
    
    @property
    def new_num(self):
        return self._new_num
    
    def reverse(self):
        return SetNumAction(self._row, self._col, self._new_num, self._orig_num)
    
class EditNoteAction(BoardAction):
    def __init__(self, row, col, num):
        super().__init__(row, col)
        self._num = num
    
    @property
    def num(self):
        return self._num
    
    def reverse(self):
        return EditNoteAction(self._row, self._col, self._num)

class SetNoteAction(BoardAction):
    def __init__(self, row, col, orig_note, new_note):
        super().__init__(row, col)
        self._orig_note = orig_note
        self._new_note = new_note
    
    @property
    def orig_note(self):
        return self._orig_note
    
    @property
    def new_note(self):
        return self._new_note
    
    def reverse(self):
        return SetNoteAction(self._row, self._col, self._new_note, self._orig_note)

class Board:

    def __init__(self, board_size):
        self._board_size = board_size
        self._matrix_size = to_matrix_size(board_size)
        self._board = [[Square(self._board_size, self._matrix_size) for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._row_digits = [0 for _ in range(self._board_size)]
        self._col_digits = [0 for _ in range(self._board_size)]
        self._matrix_digits = [0 for _ in range(self._board_size)]
        
    @property
    def row_digits(self):
        return [bin(n) for n in self._row_digits]
    
    @property
    def col_digits(self):
        return [bin(n) for n in self._col_digits]
    
    @property
    def matrix_digits(self):
        return [bin(n) for n in self._matrix_digits]
    
    def _bwn(self, num):
        return num ^ ((2**self._board_size) - 1)
    
    @staticmethod
    def _bin(num):
        return 2 ** (num - 1)
    
    def _matrix_num(self, row, col):
        return self._matrix_size[0] * (row // self._matrix_size[0]) + col // self._matrix_size[1]
    
    def _not_in_row(self, row, num):
        return self._bwn(self._row_digits[row]) & self._bin(num)

    def _not_in_col(self, col, num):
        return self._bwn(self._col_digits[col]) & self._bin(num)

    def _not_in_3x3_matrix(self, row, col, num):
        return self._bwn(self._matrix_digits[self._matrix_num(row, col)]) & self._bin(num)
    
    @property
    def board(self):
        return self._board
    
    @property
    def board_as_2darr(self):
        return [[sq.num for sq in row] for row in self._board]
    
    def load_from_2darr(self, arr):
        for row in range(len(arr)):
            for col in range(len(arr[0])):
                #self._board[row][col].set_num(arr[row][col])
                self.set_num_at(row, col, arr[row][col])
    
    @property
    def board_size(self):
        return self._board_size

    @property
    def matrix_size(self):
        return self._matrix_size

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
    
    def set_note_at(self, row, col, note):
        self._board[row][col].set_note(note)
        
    def toggle_num_at_note(self, row, col, num):
        self._board[row][col].edit_note(num) 
    
    def num_empty_squares(self):
        return sum([sum([1 for sq in row if sq.num == 0]) for row in self._board])

    def note_str(self, row, col):
        return self._board[row][col].note_str()
    
    def pieced_note_str(self, row, col, piece):
        return self._board[row][col].pieced_note_str(piece)

    @staticmethod
    def _digits_arr_hash(arr):
        return ",".join(list(map(str, arr)))

class NormalModeBoard(Board):
    def __init__(self, board_size):
        super().__init__(board_size)

    def is_safe(self, row, col, num):
        return self._not_in_row(row, num) and self._not_in_col(col, num) and self._not_in_3x3_matrix(row, col, num)

    def load(self, hash):
        sq_hash, digits_hash = hash.split("/")
        for idx, sq_hash in enumerate(sq_hash.split(";")):
            self._board[idx // self._board_size][idx % self._board_size].load(sq_hash)
        row_hash, col_hash, matrix_hash = digits_hash.split(";")
        self._row_digits = list(map(int, row_hash.split(",")))
        self._col_digits = list(map(int, col_hash.split(",")))
        self._matrix_digits = list(map(int, matrix_hash.split(",")))
    
    def hash(self):
        sq_hash = ";".join([";".join([sq.hash() for sq in row]) for row in self._board])
        digits_hash = ";".join([self._digits_arr_hash(self._row_digits), 
                                self._digits_arr_hash(self._col_digits), 
                                self._digits_arr_hash(self._matrix_digits)])
        return sq_hash + "/" + digits_hash

class KillerModeBoard(Board):
    def __init__(self, board_size):
        super().__init__(board_size)
        self._groups = {}
    
    @property
    def groups(self):
        return self._groups
    
    def is_grouped(self, row, col):
        for group, _ in self._groups.values():
            if (row, col) in group:
                return True
        return False
    
    def create_group(self, identifier, num):
        self._groups[identifier] = ([identifier], num)
    
    def add_to_group(self, identifier, square, num):
       squares, total = self._groups[identifier]
       self._groups[identifier] = (squares + [square], total + num)
    
    def adjacent_cells(self, row, col):
        cells = []
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < self._board_size and 0 <= nc < self._board_size:
                cells.append((nr, nc))
        return cells
    
    def adjacent_non_grouped_cells(self, row, col):
        return [cell for cell in self.adjacent_cells(row, col) if not self.is_grouped(cell[0], cell[1])]

    def is_group_valid(self, row, col, num):
        for squares, total in self._groups.values():
            if (row, col) in squares:
                num_filled = len([numat for sq in squares if (numat := self.get_num_at(sq[0], sq[1])) != 0]) 
                if num_filled == len(squares) - 1:
                    if sum([num if sq == (row, col) else self.get_num_at(sq[0], sq[1]) for sq in squares]) != total:
                        return False
                elif not sum([num if sq == (row, col) else self.get_num_at(sq[0], sq[1]) for sq in squares]) <= total:
                    return False
        return True     
    
    def is_safe(self, row, col, num):
        return self._not_in_row(row, num) and self._not_in_col(col, num) and self._not_in_3x3_matrix(row, col, num) and self.is_group_valid(row, col, num)

    def group_colours(self):
        colours = {}
        while len(colours) != (self._board_size ** 2):
            row, col = randint(0, self._board_size-1), randint(0, self._board_size-1)
            if (row, col) not in colours:

                for group, _ in self._groups.values():
                    if (row, col) in group:
                        break   
                possible_colours = [0, 1, 2, 3, 4]
                has_coloured_adjacent = False
                for sq in group:
                    for cell in self.adjacent_cells(sq[0], sq[1]):
                        if cell in colours and colours[cell] in possible_colours:
                            has_coloured_adjacent = True
                            possible_colours.remove(colours[cell])
                if (has_coloured_adjacent and len(colours) != 0) or len(colours) == 0:
                    colour = possible_colours[0]
                    for sq in group:
                        colours[sq] = colour
        return colours
                            