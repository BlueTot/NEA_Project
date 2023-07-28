from stack import Stack
from os import system
from abc import ABC
from colorama import Fore, Style

class UI(ABC):
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
    
    def print_board(self, board, orig_board):
        print("\n" + "    1   2   3   4   5   6   7   8   9", end='')
        for row in range(len(board)):
            print("\n" + "  " + "-"*37)
            print(row+1, end=' ')
            for col in range(len(board[0])):
                colour = Style.RESET_ALL if board[row][col] == orig_board[row][col] else Fore.BLUE
                print("|", f"{colour}{num if (num := board[row][col]) != 0 else ' '}{Style.RESET_ALL}", end = ' ')
            print("|", end='')
        print("\n" + "  " + "-"*37 + "\n")

    def print_header(self):
        system("cls")
        print("-"*11 + "\n" + "SUDOKU v0.3" + "\n" + "-"*11)
    
    def print_game_stats(self, board):
        print("\n" + "MODE: Normal")
        print("SIZE: 9")
        print(f"DIFFICULTY: {board.get_difficulty().capitalize()}")
        print(f"% COMPLETE: {round(((num_orig_empty := board.num_empty_squares(board.get_orig_board())) - board.num_empty_squares(board.get_curr_board()))/num_orig_empty * 100, 2)}%")
    
    def print_game_done(self):
        print("\n" + "You completed the game!" + "\n")
    
    def print_hint(self, hint):
        print("HINT: The valid numbers that can be placed are ", ', '.join(list(map(str, hint))))
        input("Press enter to continue")
    
    def print_message(self, message):
        input(message)
