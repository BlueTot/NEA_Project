class Stack:
    def __init__(self):
        self.__array = []
    
    def push(self, val):
        self.__array.append(val)
    
    def pop(self):
        if not self.is_empty():
            return self.__array.pop(-1)
        else:
            return -1
        
    def peek(self):
        if not self.is_empty():
            return self.__array[-1]
        else:
            return -1
    
    def is_empty(self):
        return not self.__array

class UI:
    def __init__(self):
        self._ui_stack = Stack()

class Terminal(UI):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_input(inp_string, choices):
        while True:
            choice = input(inp_string)
            if choice in choices:
                return choice
            else:
                print("Not one of the options ... try again!")
    
    def print_game_closed():
        print("Game Successfully Closed")
    
    def push_ui_to_stack(self, ui):
        self._ui_stack.push(ui)
    
    def pop_ui_from_stack(self):
        return self._ui_stack.pop()
    
    def print_board(self, board):
        print("Current Board: ")
        print()
        for row in board:
            print()
            print("-"*37)
            for num in row:
                print("|", num, end = ' ')
            print("|", end='')
        print()
        print("-"*37)
        print()

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

class Sudoku:
    def __init__(self):
        self.__ui = Terminal()

    def start(self):
        mode_choice = self.__ui.get_input("Press (T) to play game in terminal mode, (Q) to quit the game: ", ["T", "Q"])
        if mode_choice == "T":
            self.play()
        elif mode_choice == "Q":
            self.__ui.print_game_closed()
    
    def play(self):
        main_menu_choice = self.__ui.get_input("Press (P) to play game, (Q) to quit: ", ["P", "Q"])
        if main_menu_choice == "P":
            self.__ui.push_ui_to_stack("new game")
            self.__play_new_game()
        elif main_menu_choice == "Q":
            self.__ui.print_game_closed()
            return

    def __play_new_game(self):
        self.__board = Board()
        while True:
            self.__ui.print_board(self.__board.get_board())
            choice = self.__ui.get_input("Would you like to continue (Y/N): ", ["Y", "N"])
            if choice == "N":
                self.__ui.pop_ui_from_stack()
                return
            num = int(self.__ui.get_input("Enter the NUMBER you want to place: ", Board.valid_nums))
            row = int(self.__ui.get_input("Enter the ROW you want to place the number at: ", Board.valid_nums))
            col = int(self.__ui.get_input("Enter the COLUMN you want to place the number at: ", Board.valid_nums))
            self.__board.set_num_at(row, col, num)
                  
if __name__ in "__main__":
    game = Sudoku()
    game.start()
