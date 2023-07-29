from stack import Stack
from os import system
from abc import ABC, abstractmethod
from colorama import Fore, Style
from board import BoardError, Board
from game import Game

class UI(ABC):
    def __init__(self):
        self._ui_stack = Stack()
        self._push_ui_to_stack("home")
    
    def _push_ui_to_stack(self, ui):
        self._ui_stack.push(ui)
    
    def _pop_ui_from_stack(self):
        return self._ui_stack.pop()
    
    def _get_curr_ui(self):
        return self._ui_stack.peek()

    @abstractmethod
    def run(self):
        raise NotImplementedError

class Terminal(UI):

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.__print_header()
            curr_screen = self._get_curr_ui()
            if curr_screen == "home":
                self.__play_home_screen()
            elif curr_screen == "new game":
                self.__play_new_game()
            elif curr_screen == -1:
                print("Game Successfully Closed")
                return
    
    def __play_home_screen(self):
        main_menu_choice = self.__get_input("Press (P) to play game, (Q) to quit: ", ["P", "Q"])
        if main_menu_choice == "P":
            self._push_ui_to_stack("new game")
            self.__play_new_game()
        elif main_menu_choice == "Q":
            self._pop_ui_from_stack()
            return
    
    def __put_down_number(self):
        try:
            while True:
                num = int(self.__get_input("Enter the NUMBER you want to place: ", Board.VALID_NUMS))
                row = int(self.__get_input("Enter the ROW you want to place the number at: ", Board.VALID_NUMS))
                col = int(self.__get_input("Enter the COLUMN you want to place the number at: ", Board.VALID_NUMS))
                self.__game.board.set_num_at(row, col, num)
                break
        except BoardError as err:
            print(err)
    
    def __remove_number(self):
        try:
            while True:
                row = int(self.__get_input("Enter the ROW you want to remove the number at: ", Board.VALID_NUMS))
                col = int(self.__get_input("Enter the COLUMN you want to remove the number at: ", Board.VALID_NUMS))
                self.__game.board.remove_num_at(row, col)
                break
        except BoardError as err:
            print(err)
    
    def __get_hint(self):
        try:
            while True:
                row = int(self.__get_input("Enter the ROW you want to get the hint for: ", Board.VALID_NUMS))
                col = int(self.__get_input("Enter the COLUMN you want to get the hint for: ", Board.VALID_NUMS))
                return self.__game.board.get_hint_for_sq(row, col)
        except BoardError as err:
            print(err)

    def __config_game(self):
        difficulty_num = int(self.__get_input("Press (1) for Easy, (2) for Medium, (3) for Hard, (4) for Challenge: ", [str(i) for i in range(1, 5)]))
        return Board.DIFFICULTY_NUMS[difficulty_num]
    
    def __print_solution(self):
        self.__print_board(self.__game.board.get_solved_board(), self.__game.board.get_orig_board())
        print("Press enter to quit game")

    def __play_new_game(self):
        difficulty = self.__config_game()
        self.__game = Game(difficulty)
        while True:
            self.__print_header()
            self.__print_game_stats(self.__game.board)
            self.__print_curr_board()
            if self.__game.is_complete():
                print("\n" + "You completed the game!" + "\n")
                self._pop_ui_from_stack()
                return
            if self.__get_input("Would you like to quit the game? (Y/N): ", ["Y", "N"]) == "Y":
                if self.__get_input("Would you like to see the solution (Y/N): ", ["Y", "N"]) == "Y":
                    self.__print_solution()
                self._pop_ui_from_stack()
                return
            match self.__get_input("Would you like to (P)ut down a number, (R)emove a number or get a (H)int: ", ["P", "R", "H"]):
                case "P":
                    self.__put_down_number()
                case "R":
                    self.__remove_number()
                case "H":
                    if isinstance(hint := self.__get_hint(), list):
                        self.__print_hint(hint)
    
    @staticmethod
    def __get_input(inp_string, choices):
        while True:
            choice = input(inp_string)
            if choice in choices:
                return choice
            else:
                print("Not one of the options ... try again!")
    
    def __print_curr_board(self):
        self.__print_board(self.__game.board.get_curr_board(), self.__game.board.get_orig_board())

    @staticmethod
    def __print_board(board, orig_board):
        print("\n" + "    1   2   3   4   5   6   7   8   9", end='')
        for row in range(len(board)):
            print("\n" + "  " + "-"*37)
            print(row+1, end=' ')
            for col in range(len(board[0])):
                colour = Style.RESET_ALL if board[row][col] == orig_board[row][col] else Fore.BLUE
                print("|", f"{colour}{num if (num := board[row][col]) != 0 else ' '}{Style.RESET_ALL}", end = ' ')
            print("|", end='')
        print("\n" + "  " + "-"*37 + "\n")

    def __print_header(self):
        system("cls")
        print("-"*11 + "\n" + "SUDOKU v0.2.1" + "\n" + "-"*11)
    
    def __print_game_stats(self):
        print("\n" + f"MODE: {self.__game.mode}")
        print("BOARD SIZE: 9")
        print(f"DIFFICULTY: {self.__game.difficulty.capitalize()}")
        print(f"% COMPLETE: {self.__game.percent_complete()}%")

    def __print_hint(self, hint):
        print("HINT: The valid numbers that can be placed are ", ', '.join(list(map(str, hint))))
        input("Press enter to continue")
