from random import shuffle  # Import shuffle method
from copy import deepcopy  # Import deepcopy function
from dlx import DLXSolver  # Import dancing links solver


class BoardUnsolvableError(Exception):  # Board unsolvable error
    pass


class BoardSolver:  # Board Solver Class

    @staticmethod
    def __solvable(board, row=0,
                   col=0):  # Simple backtracking solver that returns True and solves the board if it is solvable, otherwise it returns False

        if col == board.board_size and row == board.board_size - 1:  # if board is filled
            return True  # return True if solvable

        if col == board.board_size:  # if reach end of row
            col = 0
            row += 1

        if board.get_num_at(row, col) > 0:  # if number is not 0
            return BoardSolver.__solvable(board, row, col + 1)  # recursively solve starting from next square

        nums_to_try = list(range(1, board.board_size + 1))  # list of numbers to try
        shuffle(nums_to_try)  # shuffle numbers so board generated doesn't follow pattern

        for num in nums_to_try:  # try all numbers
            if board.is_safe(row, col, num):  # if number is safe
                board.set_num_at(row, col, num)  # set number at (row, col)
                if BoardSolver.__solvable(board, row, col + 1):  # recursively solve starting from next square
                    return True
            board.set_num_at(row, col, 0)  # undo (set back to 0)

        return False  # return False if not solvable

    @staticmethod
    def solver(board,
               generating_mode=False):  # Solver function interface, calls DLX SOLVER if board is NormalModeBoard, otherwise calls SIMPLE BACKTRACKING SOLVER
        if board.mode == "Normal" and not generating_mode:  # if board mode is Normal
            for sol in DLXSolver.solve_sudoku(board):  # solve board using DLX
                return sol  # return board once solution is found
            raise BoardUnsolvableError  # board is not solvable
        else:
            if not BoardSolver.__solvable(new_board := deepcopy(board)):  # check if solvable on copy of board
                raise BoardUnsolvableError  # board is not solvable
            return new_board  # return copy if solvable

    @staticmethod
    def __num_solutions(board, row=0, col=0,
                        num_sols=0):  # Method to count the number of solutions using backtracking (for generating killer mode boards)

        if col == board.board_size and row == board.board_size - 1:  # if board is filled
            return num_sols + 1  # increment solution count

        if col == board.board_size:  # if reach end of row
            col = 0
            row += 1

        if board.get_num_at(row, col) > 0:  # if number is not 0
            return BoardSolver.__num_solutions(board, row, col + 1,
                                               num_sols)  # recursively solve starting from next square

        for num in range(1, board.board_size + 1):  # try all numbers
            if board.is_safe(row, col, num):  # if number can be placed (is safe)
                board.set_num_at(row, col, num)  # set number at (row, col)
                if (num_sols := BoardSolver.__num_solutions(board, row, col + 1,
                                                            num_sols)) > 1:  # check if board is still unique
                    break
            board.set_num_at(row, col, 0)  # undo (set back to 0)

        return num_sols

    def is_unique(
            board):  # Is Unique Function interface, calls DLX SOLVER if board is NormalModeBoard, otherwise calls SIMPLE BACKTRACKING SOLVER
        if board.mode == "Normal":  # if board mode is Normal
            for num_sols, _ in enumerate(DLXSolver.solve_sudoku(board)):  # check solutions using DLX
                if (num_sols + 1) > 1:  # check if number of solutions exceeds 1
                    return False
            return True
        return BoardSolver.__num_solutions(board) == 1  # otherwise check using backtracking solution checker
