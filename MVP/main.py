from ui import Terminal
from board import Board
import os

class Sudoku:
    def __init__(self):
        self.__ui = Terminal()

    def start(self):
        mode_choice = self.__ui.get_input("Press (T) to play game in terminal mode, (Q) to quit the game: ", ["T", "Q"])
        if mode_choice == "T":
            self.__ui.push_ui_to_stack("home")
            self.__play()
        elif mode_choice == "Q":
            self.__ui.print_game_closed()
    
    def __play(self):
        while True:
            os.system("cls")
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

    def __play_new_game(self):
        self.__board = Board()
        while True:
            os.system("cls")
            self.__ui.print_board(self.__board.get_board())
            choice = self.__ui.get_input("Would you like to continue (Y/N): ", ["Y", "N"])
            if choice == "N":
                if self.__ui.get_input("Would you like to see the solution (Y/N): ", ["Y", "N"]) == "Y":
                    self.__ui.print_board(self.__board.get_solved_board())
                    input("Press enter to quit game")
                self.__ui.pop_ui_from_stack()
                return
            num = int(self.__ui.get_input("Enter the NUMBER you want to place: ", Board.valid_nums))
            row = int(self.__ui.get_input("Enter the ROW you want to place the number at: ", Board.valid_nums))
            col = int(self.__ui.get_input("Enter the COLUMN you want to place the number at: ", Board.valid_nums))
            self.__board.set_num_at(row, col, num)
                  
if __name__ in "__main__":
    game = Sudoku()
    game.start()
