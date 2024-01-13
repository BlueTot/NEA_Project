from ui import UI # Import User Interface class
import os # Import os library
from colorama import Fore, Style # Import functions to print coloured text in the terminal
from game import Game # Import Game class
from game import GameError # Import GameError Exception class (for catching game errors)
from database import DBError # Import DBError Exception class (for catching database errors)

class Terminal(UI): # Terminal class, inherits from UI

    def __init__(self): # Constructor
        super().__init__() # Inheritance
        self.__notes_mode = False # User is initially not in notes mode
    
    def __valid_commands(self): # Get valid commands
        return ["E", "N", "S", "R", "help"] if self.__notes_mode else ["P", "D", "A", "H", "U", "N", "S", "R", "help"]
    
    def __help_message(self): # Get help message that is printed when user types 'help' in the terminal
        return "\nCOMMANDS: \n" + \
        ("(E) - Edit a note\n(N) - Exit notes mode\n" if self.__notes_mode else "(P) - Place a number\n(D) - Delete a number\n(H) - Get a hint\n(U) - Undo move\n(N) - Change to notes mode\n") + \
        "(S) - Save game and return to home screen\n(R) - Resign the game\n"

    def run(self): # Run method called by sudoku.py
        while True: # Main game loop
            self.__print_header() # Print game header
            curr_screen = self._get_curr_ui() # Get current screen
            match curr_screen: # Check cases of current screen and display the correct screen to the user
                case "home":
                    self.__play_home_screen()
                case "create new account":
                    self.__create_new_account()
                case "sign in":
                    self.__sign_in()
                case "manage account":
                    self.__manage_account()
                case "open or create new game":
                    self.__open_or_create_new_game()
                case "open new game":
                    self.__open_new_game()
                case "create new game":
                    self.__create_new_game()
                case "game":
                    self.__play_game()
                case -1: # UI stack is empty
                    print("Game Successfully Closed")
                    return
    
    def __play_home_screen(self): # Home screen
        # Get main menu choice from user
        if not self._application.signed_in: # Not signed in
            print("\nNOT SIGNED IN\n")
            main_menu_choice = self.__get_input("Press (P) to play sudoku, (C) to create a new account, (I) to sign in, (Q) to quit: ", ["P", "C", "I", "Q"])
        else: # Signed in
            print(f"\nSIGNED IN AS {self._application.account.username}\n")
            main_menu_choice = self.__get_input("Press (P) to play sudoku, (C) to create a new account, (M) to manage account, (O) to sign out, (Q) to quit: ", ["P", "C", "M", "O", "Q"])
        match main_menu_choice: # Check cases of main menu choice and redirect the user to the correct screen
            case "P":
                self._push_ui_to_stack("open or create new game") # Add screen to stack for main loop to render
            case "C":
                self._push_ui_to_stack("create new account")
            case "M":
                self._push_ui_to_stack("manage account")
            case "I":
                self._push_ui_to_stack("sign in")
            case "O":
                self._application.sign_out() # Call application to sign out
            case "Q":
                self._pop_ui_from_stack() # Pop current screen from stack
                return # Quit the game
    
    def __create_new_account(self): # Create new account screen
        try:
            username = self.__get_default_input("Enter username: ") # Get username
            password = self.__get_default_input("Enter password: ") # Get password
            password2 = self.__get_default_input("Enter password again: ") # Get password again
            if password == password2: # Check if passwords are the same
                self._application.create_account([username, password]) # Create account
            else:
                input("Passwords entered don't match")
        except DBError as err:
            input(err)
        self._pop_ui_from_stack()
        return
    
    def __sign_in(self): # Sign in screen
        try:
            username = self.__get_default_input("Enter username: ") # Get username
            password = self.__get_default_input("Enter password: ") # Get password
            self._application.sign_in([username, password]) # Sign in
        except DBError as err:
            input(err) # Print error in terminal if any
        self._pop_ui_from_stack()
        return
    
    def __manage_account(self): # Manage account screen
        try:
            # Get multiple choice input from user
            match self.__get_input("Would you like to change your (U)sername, change your (P)assword, (D)elete your account or go (B)ack: ", ["U", "P", "D", "B"]):
                case "U": # Change username
                    new_username = self.__get_default_input("Enter new username: ") # Get username
                    self._application.change_username(new_username) # Change username
                case "P": # Change password
                    new_password = self.__get_default_input("Enter new password: ") # Get password
                    new_password2 = self.__get_default_input("Enter new password again: ") # Get password again
                    if new_password == new_password2: # Check if passwords match
                        self._application.change_password(new_password) # Change password
                    else:
                        input("Passwords entered don't match")
                case "D": # Delete account
                    if self.__get_input("Are you sure you want to delete your account? (Y/N): ", ["Y", "N"]) == "Y": # Ask if user wants to delete their account (verification)
                        self._application.delete_account() # Delete account
                case "B": # Go back
                    pass
        except DBError as err:
            input(err) # Print error in terminal if any
        self._pop_ui_from_stack()
        return

    def __open_or_create_new_game(self): # Open or create new game screen
        if os.listdir("games"): # if there are games stored to play
            # Get multiple choice input from user
            match self.__get_input("Would you like to (O)pen a new game or (C)reate a new game, or go (B)ack to the previous screen: ", ["O", "C", "B"]):
                case "O": # open new game
                    if self._application.signed_in: # Check if user is signed in
                        if self._application.get_game_files(): # Check if user has games stored
                            self._push_ui_to_stack("open new game")
                        else:
                            input("No games saved at the moment")
                    else:
                        input("Opening games is only available if you sign in")
                case "C": # create new game
                    self._push_ui_to_stack("create new game")
                case "B":
                    self._pop_ui_from_stack()
                    return
        else:
            self._push_ui_to_stack("create new game")
    
    def __open_new_game(self): # Open new game screen
        # Print table column headings
        print((heading := f"{'No. ':^5} | {'Game':^35} | {'Creation Date':^15} | {'Creation Time':^15} | {'Mode':^15} | {'Difficulty':^15} | {'Board Size':^15}") + f"\n{'-'*len(heading)}")
        # Loop through all file names currently in user's folder
        for idx, file_name in enumerate(files := self._application.get_game_files()):
            stats = Game.get_stats_from(self._application.account.username, file_name) # Get stats dictionary
            # Print next row of table
            print(f"{idx+1:^5} | {file_name:^35} | {stats['creation date']:^15} | {stats['creation time']:^15} | {stats['mode']:^15} | {stats['difficulty']:^15} | {stats['board size']:^15}")
        while True: # Continuosly get user from user
            game_num = int(self.__get_input("Type the number of the game you want to open: ", [str(i+1) for i in range(len(files))])) # Get game number from user
            stats = Game.get_stats_from(self._application.account.username, files[game_num-1]) # Get game stats for given file
            if stats['mode'] != "Normal" or stats['board size'] != 9: # Check if user chose a game that is Normal 9x9
                input("Only Normal 9x9 Boards can be opened in terminal mode, please play in GUI mode to play other gamemodes")
            else:
                break
        self.__game = Game() # Create game
        self.__game.load_game(self._application.account.username, files[game_num-1]) # Load game from file
        self._push_ui_to_stack("game") # Redirect user to game screen

    def __create_new_game(self): # Create new game screen
        difficulty_num = int(self.__get_input("Press (1) for Easy, (2) for Medium, (3) for Hard, (4) for Expert: ", [str(i) for i in range(1, 5)])) # Get difficulty number from user
        self.__game = Game() # Create game
        self.__game.generate(mode="Normal", difficulty=Game.DIFFICULTY_NUMS[difficulty_num], board_size=9, timed=False, hardcore=False, bonus_hints=0) # Generate game based on settings
        self._push_ui_to_stack("game") # Redirect user to game screen

    def __play_game(self): # Main game screen
        while True: # game loop
            self.__print_header() # print header
            self.__print_game_stats() # print stats
            self.__print_curr_board() # print board
            if self.__game.is_complete(): # exit game if game finished
                if self._application.signed_in: # Check if user is signed in
                    self._application.save_game_stats(self.__game.get_stats(True)) # Save game stats to database
                    self.__game.remove_game_file(self._application.account.username) # Remove game file from folder if game loaded from file
                input("\n" + "You completed the game!" + "\n")
                self.__exit_to_home_screen()
                return
            if self.__notes_mode: print("\n~NOTES MODE~\n") # Notify user if they are in notes mode
            print("\nTYPE COMMAND BELOW (type 'help' for documentation)\n")
            match self.__get_input(">>> ", self.__valid_commands()): # collect input
                case "help": input(self.__help_message()) # help command
                case "P": self.__put_down_number() # place command
                case "D": self.__remove_number() # delete command
                case "A": self.__get_auto_note() # auto note command
                case "H": self.__get_hint() # hint command
                case "E": self.__edit_note() # edit note command
                case "U": self.__game.undo_last_move() # undo command
                case "N": self.__notes_mode = not self.__notes_mode # toggle notes mode command
                case "S": # save game command
                    if self._application.signed_in: # Check if user is signed in
                        self.__game.save_game(self._application.account.username) # Save game to folder
                        self.__exit_to_home_screen()
                        return
                    else:
                        input("Saving games is only available if you sign in")
                case "R": # resign game command
                    if self._application.signed_in: # Check if user is signed in
                        self._application.save_game_stats(self.__game.get_stats(False)) # Save game stats to database
                        self.__game.remove_game_file(self._application.account.username) # Remove game file from folder if game loaded from file
                    self.__print_solution()
                    self.__exit_to_home_screen()
                    return
    
    def __exit_to_home_screen(self): # Exit to home screen from game screen
        for _ in range(3): # Pop ui from stack 3 times
            self._pop_ui_from_stack()
    
    def __put_down_number(self): # Method to put down number on board
        try:
            while True:
                num = input("Enter the NUMBER you want to place: ") # Get num to place
                row = input("Enter the ROW you want to place the number at: ") # Get row
                col = input("Enter the COLUMN you want to place the number at: ") # Get col
                self.__game.put_down_number(row, col, num) # Place number
                break
        except GameError as err:
            input(err)
    
    def __remove_number(self): # Method to remove number from board
        try:
            while True:
                row = input("Enter the ROW you want to remove the number at: ") # Get row
                col = input("Enter the COLUMN you want to remove the number at: ") # Get col
                self.__game.remove_number(row, col) # Delete number
                break
        except GameError as err:
            input(err)
    
    def __get_auto_note(self): # Method to use auto note (if available)
        try:
            while True:
                row = input("Enter the ROW you want to get the auto note for: ") # Get row
                col = input("Enter the COLUMN you want to get the auto note for: ") # Get col
                self.__game.use_auto_note(row, col) # Use auto note
                break
        except GameError as err:
            input(err)
    
    def __get_hint(self): # Method to use hint (if available)
        try:
            while True:
                row = input("Enter the ROW you want to get the hint for: ") # Get row
                col = input("Enter the COLUMN you want to get the hint for: ") # Get col
                self.__game.use_hint(row, col) # Use hint
                break
        except GameError as err:
            input(err)
    
    def __edit_note(self): # Method to edit note
        try:
            while True:
                num = input("Enter the NUMBER you want to place (if the number already exists, it will be removed): ") # Get number to write
                row = input("Enter the ROW you want to edit the note at: ") # Get row
                col = input("Enter the COLUMN you want to edit the note at: ") # Get col
                self.__game.edit_note(row, col, num) # Edit note
                break
        except GameError as err:
            input(err)
    
    @staticmethod
    def __get_input(inp_string, choices): # Function to get multiple choice input from user
        while True:
            choice = input(inp_string) # Get input from user
            if choice in choices: # Check if user input is in list of choices
                return choice
            else: # Try again
                print("Not one of the options ... try again!")
    
    @staticmethod
    def __get_default_input(inp_string): # Function to get input from user (as long as the user types something)
        while True:
            choice = input(inp_string) # Get input form user
            if choice: # Check if user typed something
                return choice
            else: # Try again
                print("Please enter something ... try again!")
    
    def __print_board(self, board, orig_board): # Method to print a general board (takes two 2D arrays)
        print("\n" + (s := " "* 5 + f"{' '*5}".join(str(i) for i in range(1, 10))), end='') # Formatting
        for row in range(len(board)): # Loop through rows in the board
            print("\n" + "  " + "-"*(len(s)+1), end='')
            for piece in range(3): # Loop through the three mini-rows making up each row in the board, used to display note in 3x3 grid format
                print()
                for col in range(len(board[0])): # Loop through cols in the board
                    if (num := board[row][col].num) == orig_board[row][col].num and num != 0: # If number exists in original board (given number)
                        colour = Style.RESET_ALL # Default colour
                    elif num == 0: # No number at square (only notes)
                        colour = Fore.RED # Red
                    else: # User placed number
                        colour = Fore.BLUE # Blue
                    # Print each mini-row to the terminal, include the number at that current square if current mini-row is the middle row
                    print((f"{row+1}" if piece == 1 else " ") if col == 0 else "", 
                          "|", f"{colour}{(' '*3 if piece != 1 else f' {num} ') if (num := board[row][col].num) != 0 else self.__game.pieced_note_at(row, col, piece+1)}{Style.RESET_ALL}", 
                          end='')
                print(" |", end='') # Formatting
        print("\n" + "  " + "-"*(len(s)+1) + "\n") # Formatting
    
    def __print_curr_board(self): # Method to print current board
        self.__print_board(self.__game.curr_board, self.__game.orig_board)
    
    def __print_solution(self): # Method to print solution
        self.__print_header()
        print("\nSolution: \n")
        self.__print_board(self.__game.solved_board, self.__game.orig_board)
        input("Press enter to quit game")

    def __print_header(self): # Method to print header
        os.system("cls")
        print("-"*(l := len(s := f'SUDOKU {UI.VERSION}')) + "\n" + s + "\n" + "-"*l)
    
    def __print_game_stats(self): # Method to print game stats
        print("\n" + f"MODE: {self.__game.mode}") # Print mode
        print(f"DIFFICULTY: {self.__game.difficulty.capitalize()}") # Print difficulty
        print(f"% COMPLETE: {self.__game.percent_complete()}%") # Print percentage of filled squares
        print(f"\nAuto Notes: {self.__game.num_auto_notes_left}") # Print number of auto notes left
        print(f"Hints: {self.__game.num_hints_left}") # Print number of hints left
    