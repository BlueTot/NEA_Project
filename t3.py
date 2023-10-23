from Stage5e.dlx import solve_sudoku
from Stage5f.dlx import DLXSolver
from Stage5f.generator import *

board = BoardGenerator.new_board("Normal", "Challenge", 9)
for sol in solve_sudoku((3, 3), board.board_as_2darr):
    print(sol)
print("----------------------------")
for sol in DLXSolver.solve_sudoku(board):
    print(sol.board)

