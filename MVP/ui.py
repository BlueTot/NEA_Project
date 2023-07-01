from stack import Stack

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