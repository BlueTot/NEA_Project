from copy import deepcopy

class Board:

    valid_nums = [str(i) for i in range(1, 10)]

    def __init__(self):
        self.__size = 9
        self.__board = self.generate_new_board(self.__size)
        self.__orig_board = deepcopy(self.__board)

    @staticmethod
    def generate_new_board(size=9):
        board = [[0 for _ in range(size)] for _ in range(size)]
        return board
    
    def set_num_at(self, row, col, num):
        self.__board[row-1][col-1] = num
    
    def get_board(self):
        return self.__board
    
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
        for row in range(3*box+row, 3*(box_row + 1)):
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
    
    def get_solved_board(self):
        new_board = deepcopy(self.__orig_board)
        if self.__solve_sudoku(new_board):
            return new_board
        else:
            return -1
