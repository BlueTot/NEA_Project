from board import NormalModeBoard, KillerModeBoard
from solver import BoardSolver
from random import randint, choice
from itertools import product
from copy import deepcopy
from solver import BoardUnsolvableError
from difficulty_settings import get_num_givens

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

            while randint(0, num_squares) == 0: # each successive square in the group has a 1/n chance of generating
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

        while True:
            try:
                
                # generate a random filled board (depending on mode)
                board = BoardGenerator.__get_random_filled_board(board_size) if mode == "Normal" else BoardGenerator.get_random_filled_killer_board(board_size)
                num_remaining = board_size ** 2 # number of remaining numbers in the board
                tries = set() # set of already tried numbers

                # while there are still numbers to remove to reach the given difficulty
                while num_remaining > BoardGenerator.NUM_GIVENS[mode][board_size][difficulty]:
                    
                    # iteratively find a random filled cell
                    while board.get_num_at(row := randint(0, board_size - 1), col := randint(0, board_size - 1)) == 0:
                        pass
                    
                    # store num at (row, col) and set it to 0
                    orig_num = board.get_num_at(row, col)
                    board.set_num_at(row, col, 0)

                    # check if board only has 1 solution
                    if not BoardSolver.is_unique(deepcopy(board)):
                        
                        # undo and add cell to set of tried cells
                        board.set_num_at(row, col, orig_num) 
                        tries.add((row, col))

                        # if all possible non-empty cells have been tried
                        if len(tries) == num_remaining:
                            print("fail exit at", num_remaining, "remaining") # fail exit as board cannot be reduced further
                            return board
                    else:
                        num_remaining -= 1 # decrement number of remaining numbers
                        tries = set() # reset set of tried cells
                    
                    print(num_remaining, len(tries)) # DEBUG line of code

                return board
            
            except BoardUnsolvableError: # random filled board generated isn't solvable
                pass