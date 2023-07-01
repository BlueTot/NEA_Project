class Board:

    valid_nums = [str(i) for i in range(1, 10)]

    def __init__(self):
        self.__size = 9
        self.__board = self.generate_new_board(self.__size)

    @staticmethod
    def generate_new_board(size=9):
        board = [[0 for _ in range(size)] for _ in range(size)]
        return board
    
    def set_num_at(self, row, col, num):
        self.__board[row-1][col-1] = num
    
    def get_board(self):
        return self.__board
