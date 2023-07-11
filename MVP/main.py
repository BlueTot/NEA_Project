from ui import Terminal
from board import *

class Sudoku:

    DIFFICULTY_NUMS = {1: "easy", 2: "medium", 3: "hard", 4:"challenge"}

    def __init__(self):
        self.__ui = Terminal()

    def start(self):
        self.__ui.print_header()
        mode_choice = self.__ui.get_input("Press (T) to play game in terminal mode, (Q) to quit the game: ", ["T", "Q"])
        if mode_choice == "T":
            self.__ui.push_ui_to_stack("home")
            self.__play()
        elif mode_choice == "Q":
            self.__ui.print_game_closed()
    
    def __play(self):
        while True:
            self.__ui.print_header()
            curr_screen = self.__ui.get_curr_ui()
            if curr_screen == "home":
                self.__play_home_screen()
            elif curr_screen == "new game":
                self.__play_new_game()
            elif curr_screen == -1:
                self.__ui.print_game_closed()
                return
    
    def __play_home_screen(self):
        main_menu_choice = self.__ui.get_input("Press (P) to play game, (Q) to quit: ", ["P", "Q"])
        if main_menu_choice == "P":
            self.__ui.push_ui_to_stack("new game")
            self.__play_new_game()
        elif main_menu_choice == "Q":
            self.__ui.pop_ui_from_stack()
            return
    
    def __put_down_number(self):
        try:
            while True:
                num = int(self.__ui.get_input("Enter the NUMBER you want to place: ", Board.valid_nums))
                row = int(self.__ui.get_input("Enter the ROW you want to place the number at: ", Board.valid_nums))
                col = int(self.__ui.get_input("Enter the COLUMN you want to place the number at: ", Board.valid_nums))
                self.__board.set_num_at(row, col, num)
                break
        except InvalidNumberError:
            input(f"ERROR: {num} cannot be placed in the square ({row}, {col}) ... Press enter to continue")
        except SquareAlreadyFilledError:
            input(f"ERROR: A number already exists at the square ({row}, {col}) ... Press enter to continue")
    
    def __remove_number(self):
        try:
            while True:
                row = int(self.__ui.get_input("Enter the ROW you want to remove the number at: ", Board.valid_nums))
                col = int(self.__ui.get_input("Enter the COLUMN you want to remove the number at: ", Board.valid_nums))
                self.__board.remove_num_at(row, col)
                break
        except SquareAlreadyEmptyError:
            input(f"ERROR: There is no number at the square ({row}, {col}) that you can delete ... Press enter to continue")
        except SquareCannotBeDeletedError:
            input(f"ERROR: This square ({row}, {col}) is part of the original board and cannot be deleted ... Press enter to continue")

    def __config_game(self):
        difficulty_num = int(self.__ui.get_input("Press (1) for Easy, (2) for Medium, (3) for Hard, (4) for Challenge: ", [str(i) for i in range(1, 5)]))
        return Sudoku.DIFFICULTY_NUMS[difficulty_num]
    
    def __print_solution(self):
        self.__ui.print_board(self.__board.get_solved_board(), self.__board.get_orig_board())
        input("Press enter to quit game")


    def __play_new_game(self):
        difficulty = self.__config_game()
        self.__board = Board(difficulty)
        while True:
            self.__ui.print_header()
            self.__ui.print_game_stats(self.__board)
            self.__ui.print_board(self.__board.get_curr_board(), self.__board.get_orig_board())
            if self.__board.num_empty_squares(self.__board.get_curr_board()) == 0:
                self.__ui.print_game_done()
                self.__ui.pop_ui_from_stack()
                return
            if self.__ui.get_input("Would you like to continue (Y/N): ", ["Y", "N"]) == "N":
                if self.__ui.get_input("Would you like to see the solution (Y/N): ", ["Y", "N"]) == "Y":
                    self.__print_solution()
                self.__ui.pop_ui_from_stack()
                return
            if self.__ui.get_input("Would you like to (P)ut down a number or (R)emove a number: ", ["P", "R"]) == "P":
                self.__put_down_number()
            else:
                self.__remove_number()
            
                
if __name__ in "__main__":
    game = Sudoku()
    game.start()
