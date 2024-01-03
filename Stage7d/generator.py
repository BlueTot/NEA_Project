from board import NormalModeBoard, KillerModeBoard
from solver import BoardSolver
from random import randint, choice, shuffle
from itertools import product
from copy import deepcopy
from solver import BoardUnsolvableError
from difficulty_settings import get_num_givens
from math import sqrt, ceil

class BoardGenerator: # Board Generator Class

    NUM_GIVENS = get_num_givens()

    @staticmethod
    def __get_random_filled_board(board_size): # generate a randomly filled valid board
        board = NormalModeBoard(board_size)
        return BoardSolver.solver(board, generating_mode=True)

    @staticmethod
    def __set_groups(board): # set groups for killer sudoku board

        available_squares = list(product(range(0, board.board_size), repeat=2)) # list of squares

        while available_squares: # while there are still squares to assign a group

            base = choice(available_squares) # choose an unassigned square
            available_squares.remove(base) # remove it from the list
            board.create_group(base, board.get_num_at(base[0], base[1])) # create group at the base square
            num_squares = 0 # set number of squares in the group to 0 (n)
            curr_sq = base # set current square to the base
            while randint(0, ceil(max(num_squares - 1, 0) * 2 / sqrt(board.board_size))) == 0: # each successive square in the group has a 1/n chance of generating
                adjacent_squares = board.adjacent_non_grouped_cells(curr_sq[0], curr_sq[1]) # get adjacent non grouped cells of current cell
                if not adjacent_squares: # no adjacent squares
                    break
                adj_sq = choice(adjacent_squares) # choose an adjacent cell randomly
                available_squares.remove(adj_sq) # remove it from the list
                board.add_to_group(base, adj_sq, board.get_num_at(adj_sq[0], adj_sq[1])) #add it to the group
                curr_sq = adj_sq # set current square to the new square just added
                num_squares += 1 # increment n
        
        return board
    
    @staticmethod
    def get_random_filled_killer_board(board_size): # generate random filled killer board (with groups)
        board = KillerModeBoard(board_size) # create new killer board
        board = BoardSolver.solver(board) # randomly fill using solver
        board = BoardGenerator.__set_groups(board) # set the groups
        return board

    @staticmethod
    def new_board(mode, difficulty, board_size): # generate a new board
        
        # generate a random filled board (depending on mode)
        while True:
            try:
                board = BoardGenerator.__get_random_filled_board(board_size) if mode == "Normal" else BoardGenerator.get_random_filled_killer_board(board_size)
                break
            except BoardUnsolvableError: # keep trying until a solvable board is generated
                pass
        
        num_remaining = board_size ** 2 # number of remaining numbers in the board

        # setup list of filled cells that can be removed and shuffle it
        filled_cells = []
        for r, board_row in enumerate(board.board):
            for c, cell in enumerate(board_row):
                if cell.num != 0:
                    filled_cells.append((r, c))
        shuffle(filled_cells)

        # while there are still numbers to remove to reach the given difficulty
        while num_remaining > BoardGenerator.NUM_GIVENS[mode][board_size][difficulty]:

            for row, col in filled_cells:

                orig_num = board.get_num_at(row, col)
                board.set_num_at(row, col, 0)

                if BoardSolver.is_unique(deepcopy(board)):
                    num_remaining -= 1
                    filled_cells.remove((row, col))
                    break

                board.set_num_at(row, col, orig_num)
                filled_cells.remove((row, col))
            
            else:
                return board # exit as board cannot be reduced further (minimal board reached)

        return board # return the board when enough numbers have been removed
