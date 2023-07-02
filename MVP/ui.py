from stack import Stack
import os

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
    
    @staticmethod
    def print_game_closed():
        print("Game Successfully Closed")
    
    def push_ui_to_stack(self, ui):
        self._ui_stack.push(ui)
    
    def pop_ui_from_stack(self):
        return self._ui_stack.pop()
    
    def get_curr_ui(self):
        return self._ui_stack.peek()
    
    def print_board(self, board):
        print()
        for row in board:
            print()
            print("-"*37)
            for num in row:
                print("|", num if num != 0 else " ", end = ' ')
            print("|", end='')
        print()
        print("-"*37)
        print()

    def print_header(self):
        os.system("cls")
        print("-"*11)
        print("SUDOKU v0.1")
        print("-"*11)