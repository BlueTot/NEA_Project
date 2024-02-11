from board import NormalModeBoard, KillerModeBoard  # Import NormalModeBoard and KillerModeBoard classes
from solver import BoardSolver  # Import BoardSolver class
from random import randint, choice, shuffle  # Import random functions for generating random board
from itertools import product  # Import cartesian product function
from copy import deepcopy  # Import deepcopy function
from solver import BoardUnsolvableError  # Import BoardUnsolvableError for error-catching purposes
from difficulty_settings import get_num_givens  # Import function to get number of given numbers for a given gamemode
from math import sqrt, ceil  # Import math functions


class BoardGenerator:  # Board Generator Class

    NUM_GIVENS = get_num_givens()  # Get the number of givens allowed

    @staticmethod
    def __get_random_filled_board(board_size):  # generate a randomly filled valid board
        board = NormalModeBoard(board_size)
        return BoardSolver.solver(board, generating_mode=True)

    '''
    #######################################################################################################
    # GROUP A Skill: Complex User-Defined Algorithms - Group generator algorithm for Killer Sudoku boards #
    #                                                                                                     #
    # The KillerModeBoard class uses a complex user-defined algorithm called the Group generation         #
    # algorithm, which takes in a randomly filled valid board object and creates a dictionary             #
    # called groups that groups squares on the board together with a total.                               #
    #######################################################################################################
    '''
    @staticmethod
    def __set_groups(board):  # set groups for killer sudoku board

        available_squares = list(product(range(0, board.board_size), repeat=2))  # list of squares

        while available_squares:  # while there are still squares to assign a group

            base = choice(available_squares)  # choose an unassigned square
            available_squares.remove(base)  # remove it from the list
            board.create_group(base, board.get_num_at(base[0], base[1]))  # create group at the base square
            num_squares = 0  # set number of squares in the group to 0 (n)
            curr_sq = base  # set current square to the base
            while randint(0, ceil(max(num_squares - 1, 0) * 2 / sqrt(
                    board.board_size))) == 0:  # each successive square in the group has a 1/n chance of generating
                adjacent_squares = board.adjacent_non_grouped_cells(curr_sq[0], curr_sq[
                    1])  # get adjacent non grouped cells of current cell
                if not adjacent_squares:  # no adjacent squares
                    break
                adj_sq = choice(adjacent_squares)  # choose an adjacent cell randomly
                available_squares.remove(adj_sq)  # remove it from the list
                board.add_to_group(base, adj_sq, board.get_num_at(adj_sq[0], adj_sq[1]))  # add it to the group
                curr_sq = adj_sq  # set current square to the new square just added
                num_squares += 1  # increment n

        return board

    @staticmethod
    def get_random_filled_killer_board(board_size):  # generate random filled killer board (with groups)
        board = KillerModeBoard(board_size)  # create new killer board
        board = BoardSolver.solver(board)  # randomly fill using solver
        board = BoardGenerator.__set_groups(board)  # set the groups
        return board
    
    '''
    ###############################################################################################################################
    # GROUP A Skill: Complex User-Defined Algorithm - Board generator algorithm to generate random valid boards with one solution #
    #                                                                                                                             #
    # The Game class uses a complex user-defined board generation algorithm that creates a random filled valid board and randomly #
    # removes numbers from the board that do not cause the board to have two or more solutions. The board generation algorithm    #
    # uses the DLX solver and the simple backtracking solver to check if a board has multiple solutions.                          #
    ###############################################################################################################################
    '''
    @staticmethod
    def new_board(mode, difficulty, board_size):  # generate a new board

        # generate a random filled board (depending on mode)
        while True:
            try:
                board = BoardGenerator.__get_random_filled_board(
                    board_size) if mode == "Normal" else BoardGenerator.get_random_filled_killer_board(board_size)
                break
            except BoardUnsolvableError:  # keep trying until a solvable board is generated
                pass

        num_remaining = board_size ** 2  # number of remaining numbers in the board

        # setup list of filled cells that can be removed and shuffle it
        filled_cells = []
        for r, board_row in enumerate(board.board):
            for c, cell in enumerate(board_row):
                if cell.num != 0:
                    filled_cells.append((r, c))
        shuffle(filled_cells)  # Shuffle using random.shuffle

        # while there are still numbers to remove to reach the given difficulty
        while num_remaining > BoardGenerator.NUM_GIVENS[mode][board_size][difficulty]:

            for row, col in filled_cells:  # Iterate through all filled cells to remove

                orig_num = board.get_num_at(row, col)  # Store original number to restore later
                board.set_num_at(row, col, 0)  # Delete number at square

                if BoardSolver.is_unique(deepcopy(board)):  # Check if board still has one solution
                    num_remaining -= 1  # Decerement number of remaining numbers
                    filled_cells.remove((row, col))  # Remove from filled cells as the cell is now empty
                    break

                board.set_num_at(row, col, orig_num)  # Otherwise restore the number at that square
                filled_cells.remove((row,
                                     col))  # Remove from filled cells as cells that cannot be removed now are most likely not able to be removed in the future (as number of clues decreases)

            else:
                return board  # exit as board cannot be reduced further (minimal board reached)

        return board  # return the board when enough numbers have been removed
