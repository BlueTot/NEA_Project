from ui import UI
import os
from colorama import Fore, Style
from game import Game
from game import GameError
from database import DBError

class Terminal(UI):

    def __init__(self):
        super().__init__()
        self.__notes_mode = False
    
    def __valid_commands(self):
        return ["E", "N", "S", "R", "help"] if self.__notes_mode else ["P", "D", "H", "U", "N", "S", "R", "help"]
    
    def __help_message(self):
        return "\nCOMMANDS: \n" + \
        ("(E) - Edit a note\n(N) - Exit notes mode\n" if self.__notes_mode else "(P) - Place a number\n(D) - Delete a number\n(H) - Get a hint\n(U) - Undo move\n(N) - Change to notes mode\n") + \
        "(S) - Save game and return to home screen\n(R) - Resign the game\n"

    def run(self):
        while True:
            self.__print_header()
            curr_screen = self._get_curr_ui()
            if curr_screen == "home":
                self.__play_home_screen()
            elif curr_screen == "create new account":
                self.__create_new_account()
            elif curr_screen == "sign in":
                self.__sign_in()
            elif curr_screen == "open or create new game":
                self.__open_or_create_new_game()
            elif curr_screen == "open new game":
                self.__open_new_game()
            elif curr_screen == "create new game":
                self.__create_new_game()
            elif curr_screen == "game":
                self.__play_game()
            elif curr_screen == -1:
                print("Game Successfully Closed")
                return
    
    def __play_home_screen(self):
        if self._application.account.username is None: # Not signed in
            print("\nNOT SIGNED IN\n")
            main_menu_choice = self.__get_input("Press (S) to play singleplayer, (C) to create a new account, (I) to sign in, (Q) to quit: ", ["S", "C", "I", "Q"])
        else:
            print(f"\nSIGNED IN AS {self._application.account.username}\n")
            main_menu_choice = self.__get_input("Press (S) to play singleplayer, (C) to create a new account, (O) to sign out, (Q) to quit: ", ["S", "C", "O", "Q"])
        if main_menu_choice == "S":
            self._push_ui_to_stack("open or create new game")
        elif main_menu_choice == "C":
            self._push_ui_to_stack("create new account")
        elif main_menu_choice == "I":
            self._push_ui_to_stack("sign in")
        elif main_menu_choice == "O":
            self._application.sign_out()
        elif main_menu_choice == "Q":
            self._pop_ui_from_stack()
            return
    
    def __create_new_account(self):
        try:
            while True:
                username = self.__get_default_input("Enter username: ")
                password = self.__get_default_input("Enter password: ")
                password2 = self.__get_default_input("Enter password again: ")
                if password == password2:
                    break
                print("Passwords entered don't match ... try again!")
            self._application.create_account([username, password])
        except DBError as err:
            input(err)
        self._pop_ui_from_stack()
        return
    
    def __sign_in(self):
        while True:
            try:
                username = self.__get_default_input("Enter username: ")
                password = self.__get_default_input("Enter password: ")
                self._application.sign_in([username, password])
                self._pop_ui_from_stack()
                return
            except DBError as err:
                input(err)

    def __open_or_create_new_game(self):
        if os.listdir("games"): # if there are games stored to play
            match self.__get_input("Would you like to (O)pen a new game or (C)reate a new game: ", ["O", "C"]):
                case "O": # open new game
                    if self._application.account.username is not None:
                        if os.listdir(self._application.games_directory):
                            self._push_ui_to_stack("open new game")
                        else:
                            input("No games saved at the moment")
                    else:
                        input("Opening games is only available if you sign in")
                case "C": # create new game
                    self._push_ui_to_stack("create new game")
        else:
            self._push_ui_to_stack("create new game")
    
    def __open_new_game(self):
        print((heading := f"{'No. ':^5} | {'Game':^35} | {'Creation Date':^15} | {'Creation Time':^15} | {'Mode':^15} | {'Difficulty':^15} | {'Board Size':^15}") + f"\n{'-'*len(heading)}")
        for idx, file_name in enumerate(files := os.listdir(self._application.games_directory)):
            stats = Game.get_stats_from(file_name)
            print(f"{idx+1:^5} | {file_name:^35} | {stats['creation date']:^15} | {stats['creation time']:^15} | {stats['mode']:^15} | {stats['difficulty']:^15} | {stats['board size']:^15}")
        game_num = int(self.__get_input("Type the number of the game you want to open: ", [str(i+1) for i in range(len(files))]))
        self.__game = Game()
        self.__game.load_game(files[game_num-1])
        self._push_ui_to_stack("game")

    def __create_new_game(self):
        difficulty_num = int(self.__get_input("Press (1) for Easy, (2) for Medium, (3) for Hard, (4) for Expert: ", [str(i) for i in range(1, 5)]))
        self.__game = Game()
        self.__game.generate(mode="Normal", difficulty=Game.DIFFICULTY_NUMS[difficulty_num], board_size=9, timed=False, hardcore=False, bonus_hints=0)
        self._push_ui_to_stack("game")

    def __play_game(self):
        while True: # game loop
            self.__print_header() # print header
            self.__print_game_stats() # print stats
            self.__print_curr_board() # print board
            if self.__game.is_complete(): # exit game if game finished
                input("\n" + "You completed the game!" + "\n")
                self.__game.remove_game_file()
                self.__exit_to_home_screen()
                return
            if self.__notes_mode: print("\n~NOTES MODE~\n")
            print("\nTYPE COMMAND BELOW (type 'help' for documentation)\n")
            match self.__get_input(">>> ", self.__valid_commands()): # collect input
                case "help": input(self.__help_message()) # help command
                case "P": self.__put_down_number() # place command
                case "D": self.__remove_number() # delete command
                case "H": # hint command
                    self.__get_hint()
                case "E": self.__edit_note() # edit note command
                case "U": self.__game.undo_last_move() # undo command
                case "N": self.__notes_mode = not self.__notes_mode # toggle notes mode command
                case "S": # save game command
                    if self._application.account.username is not None:
                        self.__game.save_game(self._application.account.username)
                        input()
                        self.__exit_to_home_screen()
                        return
                    else:
                        input("Saving games is only available if you sign in")
                case "R": # resign game command
                    self.__print_solution()
                    self.__exit_to_home_screen()
                    return
    
    def __exit_to_home_screen(self):
        for _ in range(3):
            self._pop_ui_from_stack()
    
    def __put_down_number(self):
        try:
            while True:
                num = input("Enter the NUMBER you want to place: ")
                row = input("Enter the ROW you want to place the number at: ")
                col = input("Enter the COLUMN you want to place the number at: ")
                self.__game.put_down_number(row, col, num)
                break
        except GameError as err:
            input(err)
    
    def __remove_number(self):
        try:
            while True:
                row = input("Enter the ROW you want to remove the number at: ")
                col = input("Enter the COLUMN you want to remove the number at: ")
                self.__game.remove_number(row, col)
                break
        except GameError as err:
            input(err)
    
    def __get_hint(self):
        try:
            while True:
                row = input("Enter the ROW you want to get the hint for: ")
                col = input("Enter the COLUMN you want to get the hint for: ")
                self.__game.add_hint_to_notes(row, col)
                break
        except GameError as err:
            input(err)
    
    def __edit_note(self):
        try:
            while True:
                num = input("Enter the NUMBER you want to place (if the number already exists, it will be removed): ")
                row = input("Enter the ROW you want to edit the note at: ")
                col = input("Enter the COLUMN you want to edit the note at: ")
                self.__game.edit_note(row, col, num)
                break
        except GameError as err:
            input(err)
    
    @staticmethod
    def __get_input(inp_string, choices):
        while True:
            choice = input(inp_string)
            if choice in choices:
                return choice
            else:
                print("Not one of the options ... try again!")
    
    @staticmethod
    def __get_default_input(inp_string):
        while True:
            choice = input(inp_string)
            if choice:
                return choice
            else:
                print("Please enter something ... try again!")
    
    def __print_board(self, board, orig_board):
        print("\n" + (s := " "* 5 + f"{' '*5}".join(str(i) for i in range(1, 10))), end='')
        for row in range(len(board)):
            print("\n" + "  " + "-"*(len(s)+1), end='')
            for piece in range(3):
                print()
                for col in range(len(board[0])):
                    if (num := board[row][col].num) == orig_board[row][col].num and num != 0:
                        colour = Style.RESET_ALL
                    elif num == 0:
                        colour = Fore.RED
                    else:
                        colour = Fore.BLUE
                    print((f"{row+1}" if piece == 1 else " ") if col == 0 else "", 
                          "|", f"{colour}{(' '*3 if piece != 1 else f' {num} ') if (num := board[row][col].num) != 0 else self.__game.pieced_note_at(row, col, piece+1)}{Style.RESET_ALL}", 
                          end='')
                print(" |", end='')
        print("\n" + "  " + "-"*(len(s)+1) + "\n")
    
    def __print_curr_board(self):
        self.__print_board(self.__game.curr_board, self.__game.orig_board)
    
    def __print_solution(self):
        self.__print_header()
        print("\nSolution: \n")
        self.__print_board(self.__game.solved_board, self.__game.orig_board)
        input("Press enter to quit game")

    def __print_header(self):
        os.system("cls")
        print("-"*(l := len(s := f'SUDOKU {UI.VERSION}')) + "\n" + s + "\n" + "-"*l)
    
    def __print_game_stats(self):
        print("\n" + f"MODE: {self.__game.mode}")
        print(f"DIFFICULTY: {self.__game.difficulty.capitalize()}")
        print(f"% COMPLETE: {self.__game.percent_complete()}%")
    