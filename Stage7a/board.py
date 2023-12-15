from random import randint # import randint
from ast import literal_eval # importing function to convert string into list/tuple objects

def to_letter(num): # convert letter to number (A = 10 ...)
    return str(num) if 0 <= num <= 9 else chr(num-10+65)

def to_num(letter): # convert number to letter (10 = A ...)
    return int(letter) if letter.isdigit() else ord(letter) - 65 + 10

def to_matrix_size(board_size): # get matrix size from board size
    for factor in range(int(board_size ** 0.5) + 1, 0, -1):
        if board_size % factor == 0:
            return tuple(sorted((factor, board_size // factor)))

class Square: # Square class
    def __init__(self, board_size, matrix_size): # constructor (takes board size : int,  matrix size : tuple)
        self.__BOARD_SIZE = board_size
        self.__MATRIX_SIZE = matrix_size
        self.__num = 0
        self.__note = [False for _ in range(self.__BOARD_SIZE)]
    
    '''Getters'''

    @property
    def num(self): # num at square
        return self.__num
    
    @property
    def note(self): # note at square
        return self.__note
    
    '''Setters'''

    def set_num(self, num): # set num at square
        self.__num = num
    
    def set_note(self, note): # set note at square
        self.__note = note

    def edit_note(self, num): # edit note at square (toggle)
        self.__note[num - 1] = not self.__note[num - 1]
    
    '''Loading & Saving'''

    def hash(self): # return hash of square (for file save)
        return f"{self.__num},{''.join([str(num+1) for num in range(len(self.__note)) if self.__note[num]])}"
    
    def load(self, hash): # load from hash
        num, note = hash.split(",")
        self.__num = int(num)
        self.__note = [str(num+1) in note for num in range(self.__BOARD_SIZE)]

    '''Note and number rendering'''

    def note_str(self): # string representation of note (to render in gui)
        return "\n".join([" " + " ".join([to_letter(j+1) if self.__note[j] else " " for j in range(i*self.__MATRIX_SIZE[1], (i+1)*self.__MATRIX_SIZE[1])]) for i in range(self.__MATRIX_SIZE[0])])

    def pieced_note_str(self, piece): # string representation of note (to render in terminal)
        return "".join([to_letter(i+1) if self.__note[i] else " " for i in range((piece-1)*self.__MATRIX_SIZE[0], piece*self.__MATRIX_SIZE[0])])
    
    def __repr__(self): # string representation of number (DEBUG)
        return str(self.__num)

class Board: # Board Base Class

    def __init__(self, board_size): # Constructor (takes board size : int)
        self._board_size = board_size
        self._matrix_size = to_matrix_size(board_size)
        self._board = [[Square(self._board_size, self._matrix_size) for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._row_digits = [0 for _ in range(self._board_size)]
        self._col_digits = [0 for _ in range(self._board_size)]
        self._matrix_digits = [0 for _ in range(self._board_size)]
    
    def _bwn(self, num): # bitwise NOT function
        return num ^ ((2**self._board_size) - 1)
    
    @staticmethod
    def _bin(num): # convert index of number in binary number to decimal
        return 2 ** (num - 1)
    
    def matrix_num(self, row, col): # get matrix num of cell
        return self._matrix_size[0] * (row // self._matrix_size[0]) + col // self._matrix_size[1]
    
    def _not_in_row(self, row, num): # check if num isn't in row
        return self._bwn(self._row_digits[row]) & self._bin(num)

    def _not_in_col(self, col, num): # check if num isn't in col
        return self._bwn(self._col_digits[col]) & self._bin(num)

    def _not_in_3x3_matrix(self, row, col, num): # check if num isn't in matrix
        return self._bwn(self._matrix_digits[self.matrix_num(row, col)]) & self._bin(num)
    
    '''Getters'''

    @property
    def board(self): # get board (as 2D array of Square objects)
        return self._board
    
    @property
    def board_size(self): # get board size (returns int)
        return self._board_size

    @property
    def matrix_size(self): # get matrix size (returns tuple)
        return self._matrix_size

    @property
    def num_empty_squares(self): # gets number of empty squares (returns int)
        return sum([sum([1 for sq in row if sq.num == 0]) for row in self._board])
    
    def get_num_at(self, row, col): # gets number at (row, col) -> returns int
        return self._board[row][col].num

    def get_note_at(self, row, col): # gets note at (row, col) -> returns list
        return self._board[row][col].note
    
    '''Setters'''
    
    def set_num_at(self, row, col, num): # sets num at (row, col)
        if num > 0:
            self._row_digits[row] += (bin := self._bin(num)) # add binary number to row
            self._col_digits[col] += bin
            self._matrix_digits[self.matrix_num(row, col)] += bin
        elif (orig_num := self.get_num_at(row, col)) != 0:
            self._row_digits[row] -= (bin := self._bin(orig_num))
            self._col_digits[col] -= bin
            self._matrix_digits[self.matrix_num(row, col)] -= bin
        self._board[row][col].set_num(num)
    
    def set_note_at(self, row, col, note): # sets note at (row, col)
        self._board[row][col].set_note(note)
        
    def toggle_num_at_note(self, row, col, num): # toggles num at note, given (row, col)
        self._board[row][col].edit_note(num) 
    
    '''Rendering'''

    def note_str(self, row, col): # String representation of note (for rendering in GUI)
        return self._board[row][col].note_str()
    
    def pieced_note_str(self, row, col, piece): # String representation of note (for rendering in terminal)
        return self._board[row][col].pieced_note_str(piece)
    
    @property
    def board_as_2darr(self):
        return [[sq.num for sq in row] for row in self._board]
    
    def load_from_2darr(self, arr):
        for row in range(len(arr)):
            for col in range(len(arr[0])):
                self.set_num_at(row, col, arr[row][col])

class NormalModeBoard(Board): # Normal Mode Board Class

    def __init__(self, board_size): # Constructor (inherits from Board)
        super().__init__(board_size)
    
    @property
    def mode(self):
        return "Normal"

    def is_safe(self, row, col, num): # Is safe method to check if a number can be placed in a certain square
        return self._not_in_row(row, num) and self._not_in_col(col, num) and self._not_in_3x3_matrix(row, col, num) # safe only if num isn't in row, col, and matrix

    def load(self, hash): # Load method to load board from NormalModeBoard specific hash
        for idx, sq_hash in enumerate(hash.split(";")):
            self._board[row := idx // self._board_size][col := idx % self._board_size].load(sq_hash)
            self.set_num_at(row, col, self._board[row][col].num)
    
    def hash(self): # Hash method to save board (unique for NormalModeBoard)
        return ";".join([";".join([sq.hash() for sq in row]) for row in self._board])

class KillerModeBoard(Board): # Killer Mode Board Class

    def __init__(self, board_size): # Constructor (inherits from Board)
        super().__init__(board_size)
        self._groups = {} # Create groups attribute (dictionary)
    
    @property
    def mode(self):
        return "Killer"
    
    @property
    def groups(self): # Getter for groups (returns dictionary)
        return self._groups
    
    def is_grouped(self, row, col): # Check if square has already been assigned a group (returns boolean)
        for group, _ in self._groups.values():
            if (row, col) in group:
                return True
        return False
    
    def create_group(self, identifier, num): # Create a group of size 1 with a given identifier
        self._groups[identifier] = ([identifier], num)
    
    def add_to_group(self, identifier, square, num): # add square and number to the group with a given identifier
       squares, total = self._groups[identifier]
       self._groups[identifier] = (squares + [square], total + num)
    
    def adjacent_cells(self, row, col): # gets adjacent cells of a square (returns list)
        cells = []
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < self._board_size and 0 <= nc < self._board_size:
                cells.append((nr, nc))
        return cells
    
    def adjacent_non_grouped_cells(self, row, col): # gets adjacent cells of a square that aren't grouped (returns list)
        return [cell for cell in self.adjacent_cells(row, col) if not self.is_grouped(cell[0], cell[1])]

    def is_group_valid(self, row, col, num): # Check if number can be added to its group
        if not self._groups: # Return True if no groups active
            return True
        for squares, total in self._groups.values(): # Iterate through all groups
            if (row, col) in squares: # Found the group that the square is in
                num_blank = [self.get_num_at(sq[0], sq[1]) for sq in squares].count(0) # Count number of 0s
                if num_blank == 0: # Group is full
                    return sum([self.get_num_at(sq[0], sq[1]) for sq in squares]) == total # Check if sum of group is equal to total
                elif num_blank == 1: # Group is 1 away from being full
                    # Check if sum of group is equal to total including number that is being checked
                    return sum([num if sq == (row, col) else self.get_num_at(sq[0], sq[1]) for sq in squares]) == total 
                else: # Otherwise check if sum of group including number that is being checked is less than total
                    return sum([num if sq == (row, col) else self.get_num_at(sq[0], sq[1]) for sq in squares]) < total  
    
    def is_safe(self, row, col, num): # Is safe method to check if a number can be placed in a certain square
        # Is safe only if not in row, col and matrix, and group is also valid
        return self._not_in_row(row, num) and self._not_in_col(col, num) and self._not_in_3x3_matrix(row, col, num) and self.is_group_valid(row, col, num)
    
    def group_colours(self): # Assign each group a colour such that no two groups with the same colour are adjacent
        colours = {} # Initialise colours dictionary
        while len(colours) != (self._board_size ** 2): # Continue while there are still squares to be assigned colours
            row, col = randint(0, self._board_size-1), randint(0, self._board_size-1) # Choose a random square
            if (row, col) not in colours: # Check if random square hasn't been assigned a colour yet
                for group, _ in self._groups.values(): # Find the group of that square
                    if (row, col) in group:
                        break   
                possible_colours = [0, 1, 2, 3, 4] # 5 possible colours
                has_coloured_adjacent = False
                for sq in group: # iterate through all squares in the group
                    for cell in self.adjacent_cells(sq[0], sq[1]): # iterate through all adjacent cells for each square
                        if cell in colours and colours[cell] in possible_colours: # check if adjacent cell has been given a colour already
                            has_coloured_adjacent = True 
                            possible_colours.remove(colours[cell]) # remove colour from list of possible colours
                if (has_coloured_adjacent and len(colours) != 0) or len(colours) == 0: # check if no colours have been assigned yet or a neightbouring cell is already coloured
                    colour = possible_colours[0] # get a colour that isn't used by adjacent cells yet
                    for sq in group: # assign colour to all squares in the group
                        colours[sq] = colour
        return colours

    def load(self, hash): # Load board from hash (unique to KillerModeBoard)
        sqrs_hash, gp_hash = hash.split("/") # split hash into two parts
        for idx, sq_hash in enumerate(sqrs_hash.split(";")): # same for NormalModeBoard
            self._board[row := idx // self._board_size][col := idx % self._board_size].load(sq_hash)
            self.set_num_at(row, col, self._board[row][col].num)
        for pair in gp_hash.split(";"): # parse group hash
            k, v = pair.split(":")
            k, v = literal_eval(k), literal_eval(v) # convert string of tuples into tuple objects
            self._groups[k] = v
    
    def hash(self): # hash method (unique to KillerModeBoard)
        sqrs_hash = ";".join([";".join([sq.hash() for sq in row]) for row in self._board]) # generate squares hash
        gp_hash = ";".join([f"{k}:{str(v)}" for k, v in self._groups.items()]) # generate groups hash
        return sqrs_hash + "/" + gp_hash # add them together with a /
