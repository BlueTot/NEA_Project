'''Library Imports'''

from sys import argv, exit # Import argv and edit from sys
from functools import partial # Import partial from functools module
from roman import toRoman # Import roman numerals module

'''File Imports'''

from game import Game, GameError # Import Game class and GameError exception class
from ui import UI # Import UI
from board import to_letter # Import to_letter function
import database # Import database
from database import DBError # Import Database Error
from account import * # Import account, appearance config and gme milestone classes
from application import ApplicationError

'''PyQt6 GUI Imports'''

from PyQt6.QtCore import QSize, Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox
from pyqt_widgets import * # Import all customisable widget classes
  
class HomeScreen(Screen):

    # Create signals that are used to call methods in the GUI
    create_new_game_signal = pyqtSignal() # create new game
    open_existing_game_signal = pyqtSignal() # open existing game
    create_new_account_signal = pyqtSignal() # create new account
    sign_in_singal = pyqtSignal() # sign in
    sign_out_signal = pyqtSignal() # sign out
    manage_account_signal = pyqtSignal() # manage account
    view_stats_signal = pyqtSignal() # view stats
    game_milestones_signal = pyqtSignal() # game milestones
    customise_gui_signal = pyqtSignal() # customise gui
    help_signal = pyqtSignal() # help
    leaderboard_signal = pyqtSignal() # leaderboard

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name=None, create_button=False) # Inheritance

        # Title
        self.__title = Label(self, "S U D O K U", 0, 75, 1000, 125, self._application.account.app_config.title_font, 70)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__title.setStyleSheet("background: transparent;")

        # Create new game button
        self.__create_new_game_button = Button(self, "CREATE NEW GAME", 300, 250, 400, 50, self._application.account.app_config.regular_font, 25, self.__create_new_game)
        self.__create_new_game_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Open existing game button
        self.__open_existing_game_button = Button(self, "OPEN EXISTING GAME", 300, 320, 400, 50, self._application.account.app_config.regular_font, 25, self.__open_existing_game)
        self.__open_existing_game_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Leaderboard button
        self.__leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, self._application.account.app_config.regular_font, 25, self.__leaderboard_screen)
        self.__leaderboard_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Toolbar on right hand side
        self.__toolbar = ToolBar(self, size := QSize(60, 60), self._application.account.app_config.colour3, font_family := self._application.account.app_config.regular_font, font_size := 15)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.__toolbar)
        self.__toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.__quit_game, False)) # Add quit button
        if not self._application.signed_in:
            options = [("Create Account", self.__create_new_account), ("Sign In", self.__sign_in)]
        else:
            options = [("Create Account", self.__create_new_account), ("Sign Out", self.__sign_out)]
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), size, QFont(font_family, font_size), options)) # Add account button
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), size, QFont(font_family, font_size), 
                                     [("Customise GUI", self.__customise_gui), ("Manage Account", self.__manage_account)])) # Add settings button
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/stats.svg"), size, QFont(font_family, font_size), 
                                            [("Show Stats", self.__view_stats), ("Game Milestones", self.__game_milestones)])) # Add stats button
        self.__toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", self.__help_screen, False)) # Add help button

        # Current account
        self.__account_label = Label(self, "Not Signed In" if not self._application.signed_in else f"Signed in as {self._application.account.username} ({self._application.account.title} | {self._application.account.rating})", 
                                     0, 0, 450, 50, self._application.account.app_config.regular_font, 15)

        #Add to widgets (for maximising)
        self._widgets += [self.__title, self.__create_new_game_button, self.__open_existing_game_button, self.__leaderboard_button, self.__toolbar, self.__account_label]

    def __create_new_game(self): # Create new game
        self.create_new_game_signal.emit()
    
    def __open_existing_game(self): # Open existing game
        if self._application.signed_in: # If signed in
            if self._application.get_game_files(): # If there are saved games
                self.open_existing_game_signal.emit()
            else:
                self.statusBar().showMessage("*There are no saved games at this moment, please create a new game")
        else:
                self.statusBar().showMessage("*Please sign in to an account to open saved games")
    
    def __create_new_account(self): # Create new account
        self.create_new_account_signal.emit()
    
    def __sign_in(self): # Sign in
        self.sign_in_singal.emit()
    
    def __sign_out(self): # Sign out
        self.sign_out_signal.emit()
    
    def __manage_account(self): # Manage account
        if not self._application.signed_in: # If signed in
            self.statusBar().showMessage("Please sign in to manage account")
        else:
            self.manage_account_signal.emit()
    
    def __customise_gui(self): # Customise GUI
        if not self._application.signed_in: # If signed in
            self.statusBar().showMessage("Please sign in to customise GUI")
        else:
            self.customise_gui_signal.emit()
    
    def __view_stats(self): # View stats
        if not self._application.signed_in: # If signed in
            self.statusBar().showMessage("Please sign in to view stats")
        else:
            self.view_stats_signal.emit()
    
    def __game_milestones(self): # Game milestone
        if not self._application.signed_in: # If signed in
            self.statusBar().showMessage("Please sign in to view game milestones")
        else:
            self.game_milestones_signal.emit()
    
    def __help_screen(self): # Help screen
        self.help_signal.emit()

    def __leaderboard_screen(self): # Leaderboard screen
        self.leaderboard_signal.emit()

    def __quit_game(self): # Quit game
        exit()

class ConfigGameScreen(Screen): # Create new game screen

    # Create pyqt signals to connect to GUI
    return_to_home_screen_signal = pyqtSignal() # return to home screen
    play_game_signal = pyqtSignal(list) # play game

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="CREATE NEW GAME", create_button=True) # Inheritance

        # Create labels for board settings
        for idx, label in enumerate(("MODE: ", "BOARD SIZE: ", "DIFFICULTY: ", "TIMED: ", "HARDCORE: ")):
            label_obj = Label(self, label, 50, 150+75*idx, 300, 100, self._application.account.app_config.regular_font, 24)
            self._widgets.append(label_obj)
        self.__hardcore_label = Label(self, "(Hardcore enabled = No auto notes or hints allowed\n *Required to be on the leaderboard)", 50, 150+75*4+60, 500, 75, self._application.account.app_config.regular_font, 14)

        # Create menu for mode
        self.__mode_menu = ComboBox(self, 330, 175, 200, 50, self._application.account.app_config.regular_font, 20, ["Normal", "Killer"])
        self.__mode_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__mode_menu.activated.connect(self.__update_gamemode_infobox)

        # Create menu for board size
        self.__board_size_menu = ComboBox(self, 330, 250, 200, 50, self._application.account.app_config.regular_font, 20, ["4x4", "6x6", "9x9", "12x12", "16x16"])
        self.__board_size_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__board_size_menu.activated.connect(self.__update_gamemode_infobox)

        # Create menu for difficulty
        self.__difficulty_menu = ComboBox(self, 330, 325, 200, 50, self._application.account.app_config.regular_font, 20, ["Easy", "Medium", "Hard", "Expert"])
        self.__difficulty_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__difficulty_menu.activated.connect(self.__update_gamemode_infobox)

        # Create menu for timed
        self.__timed_menu = ComboBox(self, 330, 400, 200, 50, self._application.account.app_config.regular_font, 20, ["Yes", "No"])
        self.__timed_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        
        # Create menu for hardcore
        self.__hardcore_menu = ComboBox(self, 330, 475, 200, 50, self._application.account.app_config.regular_font, 20, ["Yes", "No"])
        self.__hardcore_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        
        # Create text box to show info about the gamemode that the user is selecting
        self.__gamemode_info = TextEdit(self, 650, 175, 300, 275, self._application.account.app_config.colour2, 3, self._application.account.app_config.regular_font, 18)

        # Play button
        self.__play = Button(self, "PLAY GAME", 650, 475, 300, 50, self._application.account.app_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Add to widgets (for maximising)
        self._widgets += [self.__play, self.__mode_menu, self.__difficulty_menu, 
                          self.__timed_menu, self.__board_size_menu, self.__hardcore_menu, self.__hardcore_label, self.__gamemode_info]

    def __play_game(self): # Play game
        try:
            if (difficulty := self.__difficulty_menu.currentText()) and (timed := self.__timed_menu.currentText()) and \
                (board_size := self.__board_size_menu.currentText()) and (mode := self.__mode_menu.currentText()) and \
                    (hardcore := self.__hardcore_menu.currentText()): # If all boxes have been filled
                if (mode, board_size, difficulty) in Game.DISABLED_GAMEMODES: # Check if gamemode is disabled
                    raise ApplicationError(f"*{mode} {board_size} {difficulty} is disabled due to generation issues") # Raise error
                else:
                    self.setWindowTitle("Board Generation in Progress") # Tell user that the board is currently being generated
                    self.play_game_signal.emit([mode, difficulty, int(board_size.split("x")[0]), True if timed == "Yes" else False, True if hardcore == "Yes" else False])
            else:
                raise ApplicationError("*To continue, please fill all boxes") # Raise error
        except ApplicationError as err: # Catch errors
            self.show_error(err) # Show the error
    
    def __update_gamemode_infobox(self): # Method to update gamemode info box every time user clicks the first three comboboxes
        if (difficulty := self.__difficulty_menu.currentText()) and (board_size := self.__board_size_menu.currentText()) and \
            (mode := self.__mode_menu.currentText()): # If all boxes have been filled
            if (mode, board_size, difficulty) in Game.DISABLED_GAMEMODES: # Check if gamemode has been disabled
                self.__gamemode_info.setText("This gamemode is not available") # Show text
            else:
                time_taken = self._application.get_average_time_to_complete(mode, board_size, difficulty) # Get average time to complete
                m, s = divmod(time_taken, 60) # Floor divide and mod by 60
                self.__gamemode_info.setText("".join([
                    f"Recommended Rating: {self._application.get_recommended_rating(mode, board_size, difficulty)}\n" if self._application.signed_in else "",
                    f"Average Time to Complete: {m}m {s}s"
                ])) # Set text
        else:
            self.__gamemode_info.setText("")

class OpenGameScreen(Screen): # Open game screen

    # Create pyqt signals
    play_game_signal = pyqtSignal(str) # Play game

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="OPEN EXISTING GAME", create_button=True) # Inheritance

        # Play button
        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, self._application.account.app_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Choose game label
        self.__choose_game = Label(self, "CHOOSE A GAME: ", 50, 150, 300, 100, self._application.account.app_config.regular_font, 20)

        # Choose game menu (multiple choice drop down box)
        self.__choose_game_menu = ComboBox(self, 50, 230, 400, 50,self._application.account.app_config.regular_font, 15, self._application.get_game_files())
        self.__choose_game_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__choose_game_menu.activated.connect(self.__show_game_info)

        # Game info box to display game settings
        self.__game_info = TextEdit(self, 50, 300, 400, 235, self._application.account.app_config.colour2,  2, self._application.account.app_config.regular_font, 18)

        # Add to widgets (for maximising)
        self._widgets += [self.__title, self.__play, self.__back, self.__choose_game, self.__choose_game_menu, self.__game_info]
    
    def __show_game_info(self): # Show game info
        if file := self.__choose_game_menu.currentText(): # Check if user chose a file to open
            stats = Game.get_stats_from(self._application.account.username, file) # Get stats
            labels = ["Creation Date", "Creation Time", "Mode", "Difficulty", "Board Size"] # Create labels to render
            self.__game_info.setText("\n".join([f"{label}: {stats[label.lower()]}" for label in labels])) # Render label-stat pairs in TextEdit
        else:
            self.__game_info.setText("") # Remove all existing text
    
    def __play_game(self): # Play game
        if file := self.__choose_game_menu.currentText(): # Check if user chose a file to open
            self.play_game_signal.emit(file)
        else:
            self.statusBar().showMessage("*To continue, please select a game file to play")

class GameScreen(Screen): # Main game screen

    # Constants for rendering board
    PADDING, STARTX = 25, 10 # Padding and starting x coordinate
    NUM_FONT_SIZES = {4: 20*9 // 4, 6: 20*9 // 6, 9: 20, 12: 20 * 9 // 12, 16: 20*9 // 16} # Font sizes for number
    NOTE_FONT_SIZES = {4: 13*9 // 4, 6: 13*9 // 6, 9: 13, 12: 13 * 9 // 12, 16: 5} # Font sizes for note
    TOTAL_FONT_SIZES = {4: 10*9 // 4, 6: 10*9 // 6, 9: 10, 12: 10 * 9 // 12, 16: 10 * 9 // 16} # Font sizes for total

    def __init__(self, application, max_size, game : Game): # Constructor
        
        super().__init__(application=application, max_size=max_size, title_name=None, create_button=True) # Inheritance

        self.__selected_square = (None, None) # Current selected square (nothing selected initally)
        self.__notes_mode = False # User not in notes mode initially
        self.__running = True # Game is currently running
        self.__game = game # Set game

        # Timer button and label
        self.__timer = Button(self, "", 610, 20, 130, 65, self._application.account.app_config.regular_font, 21, self.__pause_game)
        self.__timer.setStyleSheet("border: 2px solid black;")

        # Progress bar
        self.__progress = ProgressBar(self, 610, 110, 330, 20)
        self.__progress.setValue(int(self.__game.percent_complete()))
        self.__progress.setStyleSheet("QProgressBar::chunk{background-color: " + self._application.account.app_config.colour2 + ";}")

        # Info label to show game settings
        self.__info_label = Label(self, "", 595, 15, 310, 90, self._application.account.app_config.regular_font, 12)
        self.__info_label.setText(f"Mode: {self.__game.mode} \nDifficulty: {self.__game.difficulty} \nBoard Size: {self.__game.board_size}x{self.__game.board_size} \nTimed: {self.__game.timed} \nHardcore: {self.__game.hardcore}")
        self.__info_label.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black; border-radius: 30px;")
        self.__info_label.hide()

        # Info button to show/hide info label
        self.__info_button = CircularButton(self, 845, 15, 60, 60, QIcon("resources/info.svg"), self.__toggle_info_screen)

        # Undo button
        self.__undo_button = CircularButton(self, 610, 470, 58, 58, QIcon("resources/undo.svg"), self.__undo_move)

        # Auto note button
        self.__auto_note_button = CircularButton(self, 677, 470, 58, 58, QIcon("resources/auto_note.svg"), self.__show_auto_note)

        # Label to show number of auto notes left
        self.__num_auto_notes_label = Label(self, "", 681, 535, 58, 58, self._application.account.app_config.regular_font, 15)
        self.__num_auto_notes_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__num_auto_notes_label.setText(f"{self.__game.num_auto_notes_left}")

        # Hint button
        self.__hint_button = CircularButton(self, 744, 470, 58, 58, QIcon("resources/hint.svg"), self.__show_hint)

        # Label to show number of hints left
        self.__num_hints_label = Label(self, "", 748, 535, 58, 58, self._application.account.app_config.regular_font, 15)
        self.__num_hints_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if not self._application.signed_in:
            bonus_hint_str = ""
        else:
            bonus_hint_str = f'(+{bonus_hints})' if (bonus_hints := self._application.account.bonus_hints) != 0 and self.__game.num_hints_left > 0 else ''
        self.__num_hints_label.setText(f"{self.__game.num_hints_left} {bonus_hint_str}")

        # Notes button 
        self.__notes_button = CircularButton(self, 811, 470, 58, 58, QIcon("resources/notes_off.svg"), self.__toggle_notes_mode) # notes
        self.__notes_button.setIconSize(QSize(53, 53))
        self.__notes_button.setStyleSheet("border-radius: 29px; border: 5px solid black;")

        # Resign button
        self.__resign_button = CircularButton(self, 878, 470, 58, 58, QIcon("resources/resign.svg"), partial(self.__show_end_screen, False)) # resign

        # Set killer mode group colours (if any)
        if self.__game.mode == "Killer":
            self.__colours = self.__game.group_colours

        self.__create_curr_grid() # Create current grid

        # Create board cover
        self.__board_cover = Rect(self, self.STARTX+self.PADDING-3, self.PADDING-3, width:= self.GRIDSIZE*self.__game.board_size+12, height := self.GRIDSIZE*self.__game.board_size+12,
                                  self._application.account.app_config.colour2, 5)
        
        # Create paused label
        self.__paused_label = Label(self.__board_cover, "GAME PAUSED", 0, 0, width, height, self._application.account.app_config.regular_font, 24)
        self.__paused_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__board_cover.hide() # Hide the board cover and paused label


        # add to widgets (for maximising)
        self._widgets += [self.__timer, self.__info_label, self.__info_button, self.__undo_button, 
                          self.__auto_note_button, self.__hint_button, self.__num_auto_notes_label, self.__num_hints_label, self.__notes_button, 
                          self.__resign_button, self.__progress, self.__paused_label, self.__board_cover]
        
        if self.__game.timed: # If the game is timed
            self.__timer_event = QTimer() # Start a timer
            self.__timer_event.timeout.connect(self.__update_time_elapsed) # Connect method
            self.__timer_event.start(10) # Call update_time_elapsed method every 10 milliseconds (0.01 secs)
        else: # If the game is not timed
            self.__timer.setText("---") # Do not show time on the timer

    def __show_border(self, board_size, matrix_size): # Method to show board border

        big_border = Border(self, self.STARTX+self.PADDING-3, self.PADDING-3, 
                            self.GRIDSIZE*board_size+6+6, self.GRIDSIZE*board_size+6+6, 3) # Border around the board
        big_border.show() # Show the border
        self._widgets.append(big_border) # Add to widgets
        for row in range(matrix_size[1]): # Loop through all matrices on the board
            for col in range(matrix_size[0]):
                border = Border(self, self.STARTX + self.PADDING + self.GRIDSIZE*matrix_size[1]*col + 3*col, 
                                self.PADDING + self.GRIDSIZE*matrix_size[0]*row + 3*row, 
                                self.GRIDSIZE*matrix_size[1]+3, self.GRIDSIZE*matrix_size[0]+3, 3) # Create matrix borders
                border.show() # Show the border
                self._widgets.append(border) # Add to widgets

    def __create_number_grid(self, curr_board, orig_board): # Create number grid method

        BOARD_SIZE, MATRIX_SIZE = self.__game.board_size, self.__game.matrix_size # Get board size and matrix size
        self.GRIDSIZE = (560 - 2 * self.PADDING) // BOARD_SIZE # Calculate grid size

        self.__show_border(BOARD_SIZE, MATRIX_SIZE) # Show border around board

        NUM_INP_SIZE = (330 // MATRIX_SIZE[1], 330 // MATRIX_SIZE[0]) # Calculate size of input button
        STARTX, STARTY = 610, 130 # Set starting coordinates to render input buttons
        for ridx in range(MATRIX_SIZE[1]): # Loop through number of rows
            for cidx in range(MATRIX_SIZE[0]): # Loop through number of cols
                num_input = Button(self, num := to_letter(ridx*MATRIX_SIZE[0]+cidx+1), STARTX+NUM_INP_SIZE[1]*cidx, STARTY+NUM_INP_SIZE[0]*ridx, NUM_INP_SIZE[1], NUM_INP_SIZE[0], 
                                   self._application.account.app_config.regular_font, 20, partial(self.__place_num, num)) # Create input button, connected to place_num method
                num_input.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;") # Set style sheet
                self._widgets.append(num_input) # Add to widgets

        self.__sqrs = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)] # Create list of squares

        self.__num_font_size, self.__note_font_size, self.__total_font_size = self.NUM_FONT_SIZES[BOARD_SIZE], self.NOTE_FONT_SIZES[BOARD_SIZE], self.TOTAL_FONT_SIZES[BOARD_SIZE]
    
        for row, row_lst in enumerate(curr_board): # Loop through rows
            for col, sq in enumerate(row_lst): # Loop through squares
                square = Button(window = self, 
                                text = num if (num := to_letter(sq.num)) != "0" else self.__game.note_at(row, col), # Display note if num is 0
                                x = self.STARTX + self.PADDING + self.GRIDSIZE*col + MATRIX_SIZE[1]*(col//MATRIX_SIZE[1]),
                                y = self.PADDING + self.GRIDSIZE*row + MATRIX_SIZE[0]*(row//MATRIX_SIZE[0]), 
                                width = self.GRIDSIZE, 
                                height = self.GRIDSIZE, 
                                font_family = self._application.account.app_config.regular_font,
                                font_size = self.__num_font_size if sq.num != 0 else self.__note_font_size, 
                                command = partial(self.__select_square, row+1, col+1)) # Create square button
                square.setFont(QFont(self._application.account.app_config.regular_font, self.__num_font_size if sq.num != 0 else self.__note_font_size)) # Set the font
                square.setStyleSheet(f"border: {5 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + ((self._application.account.app_config.colour2 if self.__game.mode == "Normal" else "#C8C8C8") # Selected square renders as blue in NormalModeBoard, grey in KillerModeBoard
                                                           if (row+1, col+1) == self.__selected_square else 
                                                           ("white" if self.__game.mode == 'Normal' else self._application.account.app_config.killer_colours[self.__colours[(row, col)]])) + # Square renders with red/yellow/blue/green in KillerModeBoard, white in NormalModeBoard
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if sq.num != 0 else "red")) + 
                                     (";text-align: left" if sq.num == 0 else "") + 
                                     ";") # Set style sheet
                self.__sqrs[row][col] = square # Save square to list
                self._widgets.append(square) # Add to widgets
                square.show() # Show the square

                if self.__game.mode == "Killer" and (row, col) in self.__game.groups: # Create label for total of group if board is a KillerModeBoard and the square is the head of a group
                    total_label = Label(self, str(self.__game.groups[(row, col)][1]), square.x(), square.y(), square.width()//3, square.height()//3, self._application.account.app_config.regular_font, self.__total_font_size)
                    total_label.setStyleSheet("background: transparent;") # Transparent background
                    total_label.show() # Show the label
                    self._widgets.append(total_label) # Add to widgets

    def __update_number_grid(self, curr_board, orig_board): # Update number grid after every move
        mult = self._resize_factor if self.isMaximized() else 1 # Multiplying factor to maximise squares every time
        for row, row_lst in enumerate(self.__sqrs): # Loop through rows
            for col, sq in enumerate(row_lst): # Loop through squares
                sq.setText(str(num) if (num := to_letter(curr_board[row][col].num)) != "0" else self.__game.note_at(row, col)) # Update text
                sq.setFont(QFont(self._application.account.app_config.regular_font, int(mult * (self.__num_font_size if num != "0" else self.__note_font_size)))) # Update font
                sq.setStyleSheet(f"border: {3 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + 
                                     ((self._application.account.app_config.colour2 if self.__game.mode == "Normal" else "#C8C8C8") if (row+1, col+1) == self.__selected_square else ("white" if self.__game.mode == 'Normal' else self._application.account.app_config.killer_colours[self.__colours[(row, col)]])) + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if num != "0" else "red")) + 
                                     (";text-align: left" if num == "0" else "") + 
                                     ";") # Update style sheet (mainly background colour)
        self.__progress.setValue(int(self.__game.percent_complete())) # Update progress bar
    
    def __create_curr_grid(self): # Method to create current grid
        self.__create_number_grid(self.__game.curr_board, self.__game.orig_board)
    
    def __update_curr_grid(self): # Method to update current grid
        self.__update_number_grid(self.__game.curr_board, self.__game.orig_board)
    
    def __create_solution_grid(self): # Method to create solution grid after user resigns the game
        self.__create_number_grid(self.__game.solved_board, self.__game.orig_board)
    
    def __show_end_screen(self, win): # method to show game ending screen

        self.__running = False # Set running to false
        self.__selected_square = (None, None) # Reset selected square so no squares are rendered in a different colour in the solution
        self.__game.remove_game_file(self._application.account.username) # Remove game file
        if self.__game.timed: # If game is timed, stop the timer
            self.__timer_event.stop()
        if self._application.signed_in and self.__game.timed: # If signed in to an account and the game is timed
            self._application.save_game_stats(self.__game.get_stats(win))
            self._application.update_rating(rating_change := self.__game.rating_change(self._application.account.rating, win))
            self._application.update_milestone([self.__game.mode, self.__game.board_size, self.__game.difficulty, win])

        # Create translucent background rect
        bg = Rect(self, 0, 0, 1000, 560, self._application.account.app_config.colour2_translucent, 0)
        bg.show()

        # Create white window
        window = Rect(self, 200, 30, 600, 500, "white", 5) 
        window.show()

        # Create label that tells the user if they won or lost
        title = Label(self, "You Won!" if win else "Game Over!", 0, 50, 1000, 100, self._application.account.app_config.title_font, 40)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("background: transparent;")
        title.show()

        if self.__game.timed: # If the game is timed
            
            # Display time elapsed header
            time_label_top = Label(self, "Time Elapsed: ", 0, 140, 1000, 100, self._application.account.app_config.regular_font, 20)
            time_label_top.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time_label_top.setStyleSheet("background: transparent;")
            time_label_top.show()

            # Display time elapsed
            time = Label(self, self.__game.time_elapsed, 0, 180, 1000, 100, self._application.account.app_config.regular_font, 60)
            time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time.setStyleSheet("background: transparent;")
            time.show()

            if self._application.signed_in: # If signed in to an account
                
                # Display rating header
                rating_label_top = Label(self, "New Rating: ", 0, 270, 1000, 100, self._application.account.app_config.regular_font, 20)
                rating_label_top.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating_label_top.setStyleSheet("background: transparent;")
                rating_label_top.show()

                # Display rating
                rating = Label(self, rating_str := str(self._application.account.rating), 0, 310, 1000, 100, self._application.account.app_config.regular_font, 60)
                rating.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating.setStyleSheet("background: transparent;")
                rating.show()

                # Display rating change
                rating_change = Label(self, f"({f'+{rating_change}' if rating_change >= 0 else rating_change})", 60*len(rating_str), 350, 1000, 100, self._application.account.app_config.regular_font, 20)
                rating_change.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating_change.setStyleSheet("background: transparent;")
                rating_change.show()

                self._widgets += [rating_label_top, rating, rating_change] # Add to widgets
            
            self._widgets += [time, time_label_top] # Add to widgets

        # Create button to return back to home screen
        home_screen_button = Button(self, "RETURN TO HOME", 350, 450, 300, 50, self._application.account.app_config.regular_font, 20, self._return_to_home_screen)
        home_screen_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        home_screen_button.show()

        # Create button to redirect user to solution screen
        solution_button = Button(self, "SEE SOLUTION", 350, 390, 300, 50, self._application.account.app_config.regular_font, 20,self.__show_solution_screen)
        solution_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        if not win: # Show the solution button if the user resigned the game
            solution_button.show()
        
        self._widgets += [bg, window, title, home_screen_button, solution_button] # Add to widgets

        self.manualMaximise() # Manually maximise all widgets on the screen
    
    def __show_solution_screen(self): # Method to show solution screen
        
        # Create background rect to hide everything from before
        bg = Rect(self, 0, 0, 1000, 560, "white", 0)
        bg.show()
        
        self.__show_border(self.__game.board_size, self.__game.matrix_size) # Show board border
        self.__create_solution_grid() # Create solution grid

        # Create button to return back to home screen
        home_screen_button = Button(self, "RETURN TO HOME", 625, 250, 300, 50, self._application.account.app_config.regular_font, 20, self._return_to_home_screen)
        home_screen_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        home_screen_button.show()
        
        self._widgets += [bg, home_screen_button] # Add to widgets

        self.manualMaximise() # Manually maximise all widgets on the screen
    
    def __show_game_paused_error(self): # Method to show game paused error (triggered when user presses buttons that are disabled during game pause)
        self.statusBar().showMessage("ERROR: This action cannot be performed while the game is paused")

    def __select_square(self, row, col): # Method to select square on the board and update the highlighted selected square
        if self.__running: # Check if game is still running
            self.__selected_square = (row, col) # Set selected square
            self.__update_curr_grid() # Update the grid

    def __place_num(self, num): # Method to place number / remove number / edit note
        if self.__running: # Check if game is still running
            try:
                if self.__notes_mode: # If user is in notes mode
                    self.__game.edit_note(self.__selected_square[0], self.__selected_square[1], num) # Edit note
                else:
                    if self.__game.get_num_at(self.__selected_square[0], self.__selected_square[1]) == 0: # Check if number at square is 0
                        self.__game.put_down_number(self.__selected_square[0], self.__selected_square[1], num) # Place number
                    else:
                        self.__game.remove_number(self.__selected_square[0], self.__selected_square[1]) # Remove number      
            except GameError as err: # Catch GameError exceptions
                self.show_error(err) # Show error if any
            self.__update_curr_grid() # Update grid
        else:
            self.__show_game_paused_error() # Show game paused error if game is not running
        if self.__game.is_complete(): # Check if board is filled
            self.__show_end_screen(True) # Show end screen
    
    def __show_auto_note(self): # Method to use auto note
        if self.__running: # Check if game is running
            try:
                self.__game.use_auto_note(self.__selected_square[0], self.__selected_square[1]) # Use auto note
                self.__num_auto_notes_label.setText(str(self.__game.num_auto_notes_left)) # Update label showing number of auto notes left on screen
            except GameError as err:
                self.show_error(err) # Show error if any
            self.__update_curr_grid() # Update grid
        else:
            self.__show_game_paused_error() # Show game paused error if game is not running
    
    def __show_hint(self): # Method to use hint
        if self.__running: # Check if game is running
            try:
                self.__game.use_hint(self.__selected_square[0], self.__selected_square[1]) # Use hint
                if not self._application.signed_in: # No bonus hints if user is not signed in
                    bonus_hint_str = ""
                else: # Add (+k) text after number of hints left to show number of bonus hints the user currentl yhas
                    bonus_hint_str = f'(+{bonus_hints})' if (bonus_hints := self._application.account.bonus_hints) != 0 and self.__game.num_hints_left > 0 else ''
                self.__num_hints_label.setText(f"{self.__game.num_hints_left} {bonus_hint_str}") # Update number of hints left label
            except GameError as err:
                self.show_error(err) # Show error if any
            self.__update_curr_grid() # Update grid
        else:
            self.__show_game_paused_error() # Show game paused error if game is not running
    
    def __toggle_notes_mode(self): # Method to toggle between notes and normal mode
        if self.__running: # Check if game is running
            self.__notes_mode = not self.__notes_mode # Toggle notes mode variable
            self.__notes_button.setIcon(QIcon("resources/notes_on.svg" if self.__notes_mode else "resources/notes_off.svg")) # Switch icon from blue to grey / grey to blue background colour
        else:
            self.__show_game_paused_error() # Show game paused error if game is not running
    
    def __undo_move(self): # Method to undo move
        if self.__running: # Check if game is running
            self.__game.undo_last_move() # Undo move
            self.__update_curr_grid() # Update grid
        else:
            self.__show_game_paused_error() # Show game paused error if game is not running
    
    def __toggle_info_screen(self): # Toggle info screen when button is pressed
        self.__info_label.setHidden(not self.__info_label.isHidden()) # Toggle between hidden and shown
    
    def __pause_game(self): # Method to pause game
        self.__running = not self.__running # Toggle running variable
        self.__timer.setStyleSheet(f"background: {'white' if self.__running else self._application.account.app_config.colour2}; border: 2px solid black;") # Update style sheet
        self.__board_cover.setHidden(not self.__board_cover.isHidden()) # Toggle board cover between hidden and shown
        if self.__game.timed: # Check if game is timed
            if self.__running: self.__timer_event.start(10) # Start timer with 10 millisecond (0.01s) interval if game is running
            else: self.__timer_event.stop() # Stop the timer if game is not running
    
    def __update_time_elapsed(self): # Method to update time elapsed variable every 0.01 seconds
        self.__game.inc_time_elapsed() # Increment time elapsed variable
        self.__timer.setText(str(self.__game.time_elapsed)) # Update label

    def _return_to_home_screen(self): # Method to return back to home screen (Overriding existing return to home screen method)
        if self.__running and self._application.signed_in: # game quit from the "back" button
            self.__game.save_game(self._application.account.username) # Save the game to folder
        super()._return_to_home_screen() # Return to home screen

class CreateNewAccountScreen(Screen): # Create new account screen class
    
    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="CREATE NEW ACCOUNT", create_button=True) # Inheritance

        # Create username label and input box
        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create password label and input box
        self.__password = LineEdit(self, 400, 300, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create password (again) label and input box
        self.__password2 = LineEdit(self, 400, 400, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label2 = Label(self, "Enter password again: ", 100, 400, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create create account button
        self.__create = Button(self, "Create", 400, 500, 200, 50, self._application.account.app_config.regular_font, 20, self.__create_account)
        self.__create.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Add to widgets
        self._widgets += [self.__username, self.__username_label, self.__password, 
                          self.__password_label, self.__password2, self.__password_label2, self.__create]
    
    def __create_account(self): # Create account method
        if self.__username.text() and self.__password.text() and self.__password2.text(): # If user typed something in every box
            if self.__password.text() == self.__password2.text(): # If passwords match
                try:
                    self._application.create_account([self.__username.text(), self.__password.text()]) # Create account
                    self._return_to_home_screen() # Return to home screen
                except DBError as err: # Catch database error
                    self.show_error(err) # Show error on statusbar
            else:
                self.statusBar().showMessage("Passwords inputted are not the same")
        else:
            self.statusBar().showMessage("One or more input boxes are still empty")

class SignInScreen(Screen): # Sign In Screen class
    
    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="SIGN IN", create_button=True) # Inheritance

        # Create username label and input box
        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create password label and input box
        self.__password = LineEdit(self, 400, 300, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create sign in button
        self.__sign_in = Button(self, "Sign In", 400, 400, 200, 50, self._application.account.app_config.regular_font, 20, self.__sign_in)
        self.__sign_in.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Add to widgets
        self._widgets += [self.__username, self.__username_label, self.__password, 
                          self.__password_label, self.__sign_in]
    
    def __sign_in(self): # Sign in method
        if self.__username.text() and self.__password.text(): # If user typed something in both boxes
            try:
                self._application.sign_in([self.__username.text(), self.__password.text()]) # Sign in
                self._return_to_home_screen() # Return to home screen
            except DBError as err: # Catch database error
                self.show_error(err) # Show error on statusbar
        else:
            self.statusBar().showMessage("One or more input boxes are still empty")

class ViewGUIPresetsScreen(Screen): # View GUI Presets Screen class

    # Create pyqt signals
    update_preset_signal = pyqtSignal(list) # Update preset

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="VIEW PRESETS", create_button=True) # Inheritance

        # Create create preset button
        self.__create_preset = Button(self, "CREATE PRESET", 600, 180, 300, 100, self._application.account.app_config.regular_font, 22, self.__create_preset)
        self.__create_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;")

        # Create edit preset button
        self.__edit_preset = Button(self, "EDIT PRESET", 600, 310, 300, 100, self._application.account.app_config.regular_font, 22, self.__edit_preset)
        self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")

        # Create use preset button
        self.__use_preset = Button(self, "USE PRESET", 600, 440, 300, 100, self._application.account.app_config.regular_font, 22, self.__use_preset)
        self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")

        # Create current preset label
        self.__current_preset = Label(self, f"CURRENT PRESET: Preset {self._application.account.app_preset_num}",
                                       50, 150, 400, 60, self._application.account.app_config.regular_font, 20)
        
        # Create choose preset label
        self.__choose_preset = Label(self, "CHOOSE A PRESET", 50, 200, 300, 50, self._application.account.app_config.regular_font, 20)

        # Create choose preset menu (multiple choice drop down box)
        self.__choose_preset_menu = ComboBox(self, 50, 245, 400, 50,self._application.account.app_config.regular_font, 15, 
                                           [f"Preset {preset[0]}" for preset in database.get_all_presets(self._application.account.username)])
        self.__choose_preset_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__choose_preset_menu.activated.connect(self.__show_preset_info)

        # Create preset preview text edit to display contents of preset that is currently being viewed
        self.__preset_preview = TextEdit(self, 50, 325, 400, 235, self._application.account.app_config.colour2, 2, self._application.account.app_config.regular_font, 14)

        # Add widgets
        self._widgets += [self.__choose_preset, self.__choose_preset_menu, 
                          self.__create_preset, self.__edit_preset, self.__use_preset, self.__preset_preview,
                          self.__current_preset]
    
    def __create_preset(self): # Create preset method
        self.update_preset_signal.emit(["create", database.next_preset_number(self._application.account.username)]) # Redirect to edit gui preset screen

    def __edit_preset(self): # Edit preset method
        if (text := self.__choose_preset_menu.currentText()): # If user chose an option in the combobox
            if (text := self.__choose_preset_menu.currentText()) != "Preset 1": # if user did not choose Preset 1 (the default preset)
                self.update_preset_signal.emit(["edit", int(text.split(" ")[1])]) # Redirect to edit gui preset screen
            else:
                self.statusBar().showMessage("*Preset 1 is the default appearance present and cannot be edited.")
        else:
            self.statusBar().showMessage("*Please select a preset to edit")
    
    def __use_preset(self): # Use preset method
        if (text := self.__choose_preset_menu.currentText()): # If user chose an option in the combobox
            if self._application.account.app_preset_num != (num := int(text.split(" ")[1])): # If preset is not currently being used already
                self._application.use_gui_preset(num) # Use the preset
                self.__current_preset.setText(f"CURRENT PRESET: Preset {self._application.account.app_preset_num}") # Update label
            else:
                self.statusBar().showMessage(f"*Preset {num} is currently being used.") 
        else:
            self.statusBar().showMessage("*Please select a preset to use")
        
    def __show_preset_info(self): # Show preset info in textedit method
        if (text := self.__choose_preset_menu.currentText()): # If user chose an option in the combobox
            self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;") # change button colour to green
            self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;") # change button colour to green
            data = self._application.get_preset(int(text.split(" ")[1])) # get preset from database
            labels = ["Background Colour", "Colour 1", "Colour 2", "Colour 3", "Colour 4", "Title Font",
                      "Regular Font", "Killer Colour 1", "Killer Colour 2", "Killer Colour 3", "Killer Colour 4", "Killer Colour 5"] # initialise labels
            self.__preset_preview.setText("\n".join([f"{label}: {stat}" for label, stat in zip(labels, data)])) # set info box contents
        else:
            self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;") # change button colour to grey
            self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;") # change button colour to grey
            self.__preset_preview.setText("") # reset info box contents

class EditGUIPresetScreen(Screen): # Edit GUI Preset Screen Class

    def __init__(self, application, max_size, mode, preset_num): # Constructor

        super().__init__(application=application, max_size=max_size, title_name=f"{'EDIT' if mode == 'edit' else 'CREATE'} PRESET {preset_num}", create_button=True) # Inheritance

        self.__mode = mode # Set mode (create or edit)
        self.__preset_num = preset_num # Set preset number of preset that is being created or edited

        self.__curr_preset = self._application.get_preset(preset_num) # Get current preset being edited

        # Create labels on the left
        for idx, label in enumerate(("Background Colour", "Colour 1", "Colour 2", "Colour 3", "Colour 4", "Title Font")):
            label_obj = Label(self, label, 50, 150+60*idx, 300, 40, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)
        
        # Create labels on the right
        for idx, label in enumerate(("Regular Font", "Killer Colour 1", "Killer Colour 2", "Killer Colour 3", "Killer Colour 4", "Killer Colour 5")):
            label_obj = Label(self, label, 575, 150+60*idx, 300, 40, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)
        
        # Create input boxes for user to type in colours (on the left)
        self.__bg_colour = LineEdit(self, 325, 150, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[0], False)
        self.__colour1 = LineEdit(self, 325, 210, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[1], False)
        self.__colour2 = LineEdit(self, 325, 270, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[2], False)
        self.__colour3 = LineEdit(self, 325, 330, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[3], False)
        self.__colour4 = LineEdit(self, 325, 390, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[4], False)

        # Combo box for user to choose title font from list of system fonts
        self.__title_font = ComboBox(self, 325, 450, 200, 50, self._application.account.app_config.regular_font, 14, QFontDatabase.families(), add_blank=False)
        self.__title_font.setCurrentText(self.__curr_preset[5])
        self.__title_font.setStyleSheet(f"background: white; border: 2px solid black;")
        
        # Combo box for user to choose regular font from list of system fonts
        self.__regular_font = ComboBox(self, 775, 150, 200, 50, self._application.account.app_config.regular_font, 14, QFontDatabase.families(), add_blank=False)
        self.__regular_font.setCurrentText(self.__curr_preset[6])
        self.__regular_font.setStyleSheet(f"background: white; border: 2px solid black;")
        
        # Create input boxes for user to type in colours (on the right)
        self.__killer_colour1 = LineEdit(self, 775, 210, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[7], False)
        self.__killer_colour2 = LineEdit(self, 775, 270, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[8], False)
        self.__killer_colour3 = LineEdit(self, 775, 330, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[9], False)
        self.__killer_colour4 = LineEdit(self, 775, 390, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[10], False)
        self.__killer_colour5 = LineEdit(self, 775, 450, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[11], False)

        # Create list of options for easy access later
        self.__options = [self.__bg_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__killer_colour1, 
                          self.__killer_colour2, self.__killer_colour3, self.__killer_colour4, self.__killer_colour5]

        # Create save preset button
        self.__save = Button(self, "Save Changes", 275, 525, 200, 50, self._application.account.app_config.regular_font, 18, self.__save)
        self.__save.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Create delete preset button
        self.__delete = Button(self, "Delete Preset", 525, 525, 200, 50, self._application.account.app_config.regular_font, 18, self.__delete)
        self.__delete.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Add to widgets
        self._widgets += [self.__bg_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__title_font, 
                          self.__regular_font, self.__killer_colour1, self.__killer_colour2, self.__killer_colour3, self.__killer_colour4, self.__killer_colour5,
                          self.__save, self.__delete]
    
    def __get_options(self): # Method to get contents of input boxes (returns list)
        options = [text if (text := textbox.text()) else textbox.placeholderText() for textbox in self.__options]
        combo_boxes = [self.__title_font.currentText(), self.__regular_font.currentText()]
        return options[0:5] + combo_boxes + options[5:]
    
    def __font_options_changed(self): # Method to check if font options have been changed from previously saved settings
        data = self._application.get_preset(self.__preset_num)
        return self.__title_font.currentText() != data[5] or self.__regular_font.currentText() != data[6]
    
    def __save(self): # save preset method
        options = self.__get_options() # get contents of input boxes
        if any([textbox.text() for textbox in self.__options]) or self.__font_options_changed(): # check if at least one option is changed
            self._application.update_appearance_preset([self.__mode, self.__preset_num] + options) # save preset
            self._return_to_home_screen() # return to home screen
        else:
            self.statusBar().showMessage("Please fill in at least one box to save")
    
    def __delete(self): # delete preset method
        if self._application.account.app_preset_num == self.__preset_num: # check if preset is currently being used
            self.statusBar().showMessage("*Preset is currently in use and cannot be deleted.") # display error message
        else: # otherwise
            self._application.delete_appearance_preset(self.__preset_num) # delete preset
            self._return_to_home_screen() # return to home screen

class ManageAccountScreen(Screen): # Manage account screen class
    
    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="MANAGE ACCOUNT", create_button=True) # Inheritance

        # Create labels
        for idx, label in enumerate(("Change Username", "Old Password", "New Password", "New Password Again")):
            label_obj = Label(self, label, 100, 200+75*idx, 300, 50, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)

        # Create username, old password, new password and new password (again) input boxes for user to type in
        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, f"Current username: {self._application.account.username}", False)
        self.__old_password = LineEdit(self, 400, 275, 500, 50, self._application.account.app_config.regular_font, 15, "**************", True)
        self.__new_password = LineEdit(self, 400, 350, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__new_password2 = LineEdit(self, 400, 425, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__textboxes = [self.__username, self.__old_password, self.__new_password, self.__new_password2]

        # Create save changes button
        self.__save = Button(self, "Save Changes", 275, 500, 200, 50, self._application.account.app_config.regular_font, 18, self.__save)
        self.__save.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        # Create delete account button
        self.__delete = Button(self, "Delete Account", 525, 500, 200, 50, self._application.account.app_config.regular_font, 18, self.__delete)
        self.__delete.setStyleSheet(f"background: {self._application.account.app_config.colour4}; border: 2px solid black;")

        self._widgets += [self.__username, self.__old_password, self.__new_password, 
                          self.__new_password2, self.__save, self.__delete]
    
    def __save(self): # Save account changes method
        try:
            change_username, change_password = False, False
            if not any([textbox.text() for textbox in self.__textboxes]): # Check if user did not type anything
                raise ApplicationError("Please either change your username or password to save")
            if (username := self.__username.text()): # If user typed their username
                change_username = True        
            if all([textbox.text() for textbox in self.__textboxes[1:]]): # If user wishes to change their password
                if not self._application.check_password_match(self.__old_password.text()): # check if old passwords don't match
                    raise ApplicationError("Incorrect original password")
                if self.__new_password.text() != self.__new_password2.text(): # check if new don't passwords match
                    raise ApplicationError("New passwords inputted are not the same")
                if self.__new_password.text() == self.__old_password.text(): # check if new password is different to old password
                    raise ApplicationError("Please choose a different password to your current one")
                change_password = True
            if change_username:
                self._application.change_username(username)
            if change_password:
                self._application.change_password(self.__new_password.text())
            self._return_to_home_screen() # return to home screen
        except DBError as err: # Catch database errors
            self.show_error(err)
        except ApplicationError as err: # Catch application errors
            self.show_error(err) # Show error

    def __delete(self): # delete account method
        self.__message_box = QMessageBox(self) # create message box to ask user if they really want to delete their account
        self.__message_box.setWindowTitle("Delete Account Menu") # set title
        self.__message_box.setText("Are you sure you want to delete your account?") # set text
        self.__message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) # add yes and no buttons
        self.__message_box.buttonClicked.connect(self.__delete_menu_button) # connect to next method
        self.__message_box.show() # show the message box
    
    def __delete_menu_button(self, button): # method to delete account when user confirms
        if button.text()[1:] == "Yes": # check if user pressed yes
            self._application.delete_account()
            self._return_to_home_screen() # return to home screen

class ViewStatsScreen(Screen): # View stats screen class
    
    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="PLAYER STATS", create_button=True) # Inheritance
        
        # Create stats text edit widget
        self.__stats = TextEdit(self, 50, 150, 400, 450, self._application.account.app_config.colour2_translucent, 4, self._application.account.app_config.regular_font, 18)

        # Get number of total games and number of completed games
        total_games = database.num_of_games(self._application.account.username)
        completed_games = database.num_completed_games(self._application.account.username)

        # Convert text into string to insert into widget
        stats_txt = "\n".join([
        "OVERALL STATS: \n",
        f"Rating: {self._application.account.rating}",                         
        f"Title: {self._application.account.title}\n",
        f"Total Games Played: {total_games}",
        f"Completed Games: {completed_games}",
        f"% Complete: {f'{round(completed_games/total_games*100)}%' if total_games != 0 else 'N/A'}\n",
        f"Num of Bonus Hints: {self._application.account.bonus_hints}"
        ])
    
        self.__stats.insertPlainText(stats_txt) # Insert text

        # Create labels
        for idx, label in enumerate(["Mode", "Board Size", "Difficulty"]):
            label_obj = Label(self, label, 525, 150+idx*60, 200, 45, self._application.account.app_config.regular_font, 20)
            self._widgets.append(label_obj)

        # Create menus to choose which stats to view
        self.__mode_menu = ComboBox(self, 700, 150, 200, 45, self._application.account.app_config.regular_font, 20, ["Normal", "Killer"])
        self.__mode_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__mode_menu.activated.connect(self.update_gamemode_stats)
        self.__board_size_menu = ComboBox(self, 700, 210, 200, 45, self._application.account.app_config.regular_font, 20, ["4x4", "6x6", "9x9", "12x12", "16x16"])
        self.__board_size_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__board_size_menu.activated.connect(self.update_gamemode_stats)
        self.__difficulty_menu = ComboBox(self, 700, 270, 200, 45, self._application.account.app_config.regular_font, 20, ["Easy", "Medium", "Hard", "Expert"])
        self.__difficulty_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__difficulty_menu.activated.connect(self.update_gamemode_stats)

        # create stats text edit widget
        self.__gamemode_stats = TextEdit(self, 525, 350, 400, 250, self._application.account.app_config.colour2_translucent, 4, self._application.account.app_config.regular_font, 18)

        # Add to widgets
        self._widgets += [self.__stats, self.__mode_menu, self.__board_size_menu, 
                          self.__difficulty_menu, self.__gamemode_stats]
    
    def update_gamemode_stats(self): # Method to update gamemode stats
        if self.__mode_menu.currentText() and self.__board_size_menu.currentText() and self.__difficulty_menu.currentText(): # Check if user typed something in all three boxes
            # Get mode, board size and difficulty
            mode, board_size, difficulty = self.__mode_menu.currentText(), int(self.__board_size_menu.currentText().split("x")[0]), self.__difficulty_menu.currentText()
            self.__gamemode_stats.setText("\n".join([
                f"Times Played: {database.times_played(self._application.account.username, mode, board_size, difficulty)}",
                f"Number of Completions: {database.num_completions(self._application.account.username, mode, board_size, difficulty)}",
                f"Best Time: {database.best_time(self._application.account.username, mode, board_size, difficulty)}",
                f"Best Hardcore Time: {database.best_hardcore_time(self._application.account.username, mode, board_size, difficulty)}"
            ])) # Set text in gamemode stats text edit

class GameMilestonesScreen(Screen): # Game Milestones Screen class
    
    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="GAME MILESTONES", create_button=True) # Inheritance
        
        # Create currently selected milestone
        self.__selected_milestone = None

        # Create board size labels
        for idx, label in enumerate(milestone_types := ("4x4", "6x6", "9x9", "12x12", "16x16")):
            label = Label(self, label, 50, 175+80*idx, 100, 50, self._application.account.app_config.regular_font, 30)
            self._widgets.append(label)

        milestone_claimed = self._application.account.milestone_claimed # Get milestone claimed string
        self.__milestone_buttons = {} # Setup dictionary of milestone buttons
        for vidx, board_size in enumerate(milestone_types): # Loop through milestone types
            for hidx, milestone_num in enumerate(range(1, 8)): # Loop through 7 reward tiers
                box = Button(self, toRoman(milestone_num), x := 200+hidx*70, y := 175+80*vidx, 60, 60, 
                             self._application.account.app_config.title_font, 22, 
                             partial(self.__view_game_milestone, board_size, milestone_num)) # Create reward box
                box.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) else 'rgb(175, 175, 175)'}; border: 3px solid black;") # Set style sheet
                unclaimed_label = Label(self, "!" if int(milestone_claimed[vidx*7+hidx]) else "", x+48, y+5, 14, 14, 
                                        self._application.account.app_config.regular_font, 14) # Set label to show if reward is unlocked but unclaimed
                unclaimed_label.setStyleSheet("background: transparent; color: red;") # Set colour to red
                self.__milestone_buttons[(vidx, hidx)] = (board_size, milestone_num, box, unclaimed_label) # Add to dictionary
                self._widgets.extend([box, unclaimed_label]) # Add to widgets
        
        self.__milestone_data_box = TextEdit(self, 725, 175, 250, 330, self._application.account.app_config.colour2_translucent, 3, 
                                             self._application.account.app_config.regular_font, 16) # Create text box to show details about milestone reward
        self.__claim_reward = Button(self, "Claim Reward", 725, 515, 250, 40, self._application.account.app_config.regular_font, 18, self.__claim_reward) # Create claim reward button
        self.__claim_reward.setStyleSheet("background: rgb(175, 175, 175); border: 2px solid black;") # Set background colour
            
        self._widgets += [self.__milestone_data_box, self.__claim_reward] # Add to widgets
    
    def __update_milestone_grid(self): # Method to update milestone grid
        milestone_claimed = self._application.account.milestone_claimed # Get milestone claimed string
        for k, v in self.__milestone_buttons.items(): # Loop through all milestone buttons
            vidx, hidx = k # Get vertical box number and horizontal box number
            board_size, milestone_num, box, unclaimed_label = v # Get board size, milestone number, box and unclaimed label (!)
            box.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) else 'rgb(175, 175, 175)'}; border: 3px solid black;") # Update style sheet
            unclaimed_label.setText("!" if int(milestone_claimed[vidx*7+hidx]) else "") # Set unclaimed label (!)
        self.__view_game_milestone(self.__selected_milestone[0], self.__selected_milestone[1]) # View game milestone for the currently selected milestone

    def __complete(self, board_size, milestone_num): # Method to check if a milestone reward can be claimed
        milestone = database.milestone(self._application.account.username, f"milestone_{board_size}")
        return milestone >= GameMilestones.MILESTONES[int(milestone_num)]
    
    def __parse_reward(self, reward): # Method to parse the reward string
        if reward is None: # No reward
            return "None"
        elif reward[0] == "H": # Hint reward
            return f"+{reward[1]} Hint(s)"
    
    def __selected_milestone_not_claimed(self): # Method to check if the currently selected milestone reward hasn't been claimed
        board_size, milestone_num = self.__selected_milestone # get board size and milestone number
        claimed = self._application.account.milestone_claimed # get claimed string
        idx = GameMilestones.BOARD_SIZE_IDXS[int(board_size.split("x")[0])] * 7 + int(milestone_num) - 1 # get index of reward
        return int(claimed[idx]) # get bit at index in string
    
    def __view_game_milestone(self, board_size, milestone_num): # Method to view game milestone on text edit
        self.__selected_milestone = (board_size, milestone_num) # set current selected milestone
        milestone = database.milestone(self._application.account.username, f"milestone_{board_size}") # get milestone number
        status = "Complete" if self.__complete(board_size, milestone_num) else "Incomplete" # Set completion status of milestone
        target = GameMilestones.MILESTONES[int(milestone_num)] # Get target milestone number
        self.__milestone_data_box.setText("\n".join([
            f"{board_size} MILESTONE {toRoman(milestone_num)}: \n",
            f"Status: {status}",
            f"Progress: {milestone}/{target} ({round(milestone/target*100)}%)\n",
            f"Reward: {self.__parse_reward(GameMilestones.REWARDS[board_size][int(milestone_num)])}"
        ])) # Set text in milestone data box
        self.__claim_reward.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) and self.__selected_milestone_not_claimed() else 'rgb(175, 175, 175)'}; border: 3px solid black;") # Set style sheet
    
    def __claim_reward(self): # Method to claim reward
        if self.__selected_milestone is not None: # Check if user selected a milestone
            if self.__complete(self.__selected_milestone[0], self.__selected_milestone[1]): # Check if the milestone has been reached
                if self.__selected_milestone_not_claimed(): # Check if the milestone reward hasn't been claimed yet
                    self._application.claim_reward([int(self.__selected_milestone[0].split("x")[0]), int(self.__selected_milestone[1])]) # Claim milestone
                    self.__update_milestone_grid() # Update milestone grid
                else:
                    self.statusBar().showMessage("You already claimed this reward!")
            else:
                self.statusBar().showMessage("You haven't unlocked this reward yet!")
        else:
            self.statusBar().showMessage("Please select a milestone to claim")

class HelpScreen(Screen): # Help Screen class

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name=None, create_button=True) # Inheritance

        self.setStyleSheet(f"background: {self._application.account.app_config.colour3};") # Set background colour of screen
        
        # Create help instructions text window
        self.__txt_window = TextEdit(self, 100, 20, 800, 520, "white", 5, self._application.account.app_config.regular_font, 16)
        with open("resources/help.txt", "r") as f: # Open help.txt file and insert the text read in
            self.__txt_window.insertPlainText(f.read())

        self._widgets += [self.__txt_window] # Add to widgets

class LeaderboardScreen(Screen): # Leaderboard Screen Class

    def __init__(self, application, max_size): # Constructor

        super().__init__(application=application, max_size=max_size, title_name="LEADERBOARD", create_button=True) # Inheritance

        # Create leaderboard table
        self.__table = TableWidget(self, 50, 125, 600, 450, self._application.account.app_config.regular_font, 18, self._application.account.app_config.colour2_translucent, 25, 3)
        self.__show_default_leaderboard() # Method to show default leaderboard contents

        # Create gamemode options
        gamemode_options = []
        for mode in ("Normal", "Killer"):
            for board_size in (milestone_options := ["4x4", "6x6", "9x9", "12x12", "16x16"]):
                for difficulty in ("Easy", "Medium", "Hard", "Expert"):
                    gamemode_options.append(f"{mode} {board_size} {difficulty}")

        # Create leaderboard options label
        self.__type_label = Label(self, "Leaderboard Options", 700, 125, 250, 40, self._application.account.app_config.regular_font, 18)
        
        # Create drop down menu where user can choose to view best time or milestone stats
        self.__type = ComboBox(self, 700, 175, 250, 40, self._application.account.app_config.regular_font, 18, ["Best Time", "Milestone"])
        self.__type.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__type.activated.connect(self.__show_options)

        # Next drop down menu label
        self.__next_label = Label(self, "", 700, 225, 250, 40, self._application.account.app_config.regular_font, 18)

        # Gamemode drop down menu
        self.__gamemode = ComboBox(self, 700, 275, 250, 40, self._application.account.app_config.regular_font, 18, gamemode_options)
        self.__gamemode.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__gamemode.activated.connect(partial(self.__update_table, "gamemode"))
        self.__gamemode.hide() # Hide for now

        # Milestone drop down menu
        self.__milestone = ComboBox(self, 700, 275, 250, 40, self._application.account.app_config.regular_font, 18, milestone_options)
        self.__milestone.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__milestone.activated.connect(partial(self.__update_table, "milestone"))
        self.__milestone.hide() # Hide for now

        # Add to widgets
        self._widgets += [self.__table, self.__type, self.__gamemode, 
                          self.__milestone, self.__type_label, self.__next_label]  
    
    def __show_options(self): # Method to show current options for best time or milestone
        if self.__type.currentText() == "Best Time": # If user chose to see best time details
            self.__gamemode.setCurrentText("") # Reset gamemode combobox contents
            self.__gamemode.show() # Show gamemode combobox
            self.__milestone.hide() # Hide milestone combobox
            self.__next_label.setText("Choose Gamemode") # Set label text
            self.__show_default_leaderboard()
        elif self.__type.currentText() == "Milestone": # If user chose to see milestone details
            self.__gamemode.hide() # Hide gamemode combobox
            self.__milestone.setCurrentText("") # Reset milestone combobox contents
            self.__milestone.show() # Show milestone combobox
            self.__next_label.setText("Choose Milestone") # Set label text
            self.__show_default_leaderboard()
        else:
            self.__gamemode.hide() # Hide gamemode combobox
            self.__milestone.hide() # Hide milestone combobox
            self.__next_label.setText("") # Reset label text
            self.__show_default_leaderboard() # Show default leaderboard contents
    
    def __show_default_leaderboard(self): # Method to show default leaderboard contents
        headings = ["Player Username", "Rating", "Title"] # Set headings
        self.__table.load_data(headings, database.all_account_rating_data()) # Load data with contents
    
    def __update_table(self, mode): # Method to update table
        if mode == "gamemode" and (txt := self.__gamemode.currentText()): # If user chose to see gamemode best time stats and user chose an option in the gamemode combobox
            mode, bs, difficulty = txt.split(" ") # Get mode, board size and difficulty
            board_size = int(bs.split("x")[0]) # Convert board size to integer
            headings = ["Player Username", "Rating", "Title", f"Best Time ({txt})"] # Set headings
            self.__table.load_data(headings, database.leaderboard_best_time_data(mode, board_size, difficulty)) # Load data with contents
        elif mode == "milestone" and (board_size := self.__milestone.currentText()): # If user chose to see milestone stats and user chose an option in the milestone combobox
            headings = ["Player Username", "Rating", "Title", f"Milestone Completions ({board_size})"] # Set headings
            self.__table.load_data(headings, database.leaderboard_milestone_data(board_size)) # Load data with contents
        else: # Otherwise
            self.__show_default_leaderboard() # Show the default leaderboard
            self.statusBar().showMessage("Please select an option to continue") # Show error message

class GUI(UI): # Graphical User Interface (GUI) class

    def __init__(self): # Constructor

        super().__init__() # Inherit from UI

        self.__pyqt_app = QApplication(argv) # Create PyQt GUI Application
        self.__max_size = self.__pyqt_app.primaryScreen().size() # Create maximum size (for maximising the window)
        
        self.__options = {"full screen": True} # Default options dictionary

        # Initialise fonts used in GUI
        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        self.__screens = {} # Placeholder screens dictionary to make it easier to load and render screens
        self.__screen_partials = {"home": self.__home_screen,
                                  "config game": self.__config_game_screen, "open game": self.__open_game_screen,
                                  "game": self.__game_screen, "create new account": self.__create_new_account_screen, 
                                  "sign in": self.__sign_in_screen, "manage account": self.__manage_account_screen, 
                                  "view stats": self.__view_stats_screen, "game milestones": self.__game_milestones_screen,
                                  "view gui presets": self.__view_gui_presets_screen,
                                  "edit gui preset": self.__edit_gui_preset_screen, "help": self.__help_screen,
                                  "leaderboard": self.__leaderboard_screen} # Dictionary of screen partials used to initialise each screen
        self.__show_screen("home", self.__screen_partials["home"]) # Show the home screen
    
    def __home_screen(self): # Initialise home screen
        home_screen = HomeScreen(self._application, self.__max_size)
        home_screen.create_new_game_signal.connect(partial(self.__show_screen, "config game", self.__config_game_screen))
        home_screen.open_existing_game_signal.connect(partial(self.__show_screen, "open game", self.__open_game_screen))
        home_screen.create_new_account_signal.connect(partial(self.__show_screen, "create new account", self.__create_new_account_screen))
        home_screen.sign_in_singal.connect(partial(self.__show_screen, "sign in", self.__sign_in_screen))
        home_screen.sign_out_signal.connect(self.__sign_out)
        home_screen.manage_account_signal.connect(partial(self.__show_screen, "manage account", self.__manage_account_screen))
        home_screen.customise_gui_signal.connect(partial(self.__show_screen, "view gui presets", self.__view_gui_presets_screen))
        home_screen.view_stats_signal.connect(partial(self.__show_screen, "view stats", self.__view_stats_screen))
        home_screen.game_milestones_signal.connect(partial(self.__show_screen, "game milestones", self.__game_milestones_screen))
        home_screen.help_signal.connect(partial(self.__show_screen, "help", self.__help_screen))
        home_screen.leaderboard_signal.connect(partial(self.__show_screen, "leaderboard", self.__leaderboard_screen))
        return home_screen
    
    def __open_game_screen(self): # Initialise open game screen
        open_game_screen = OpenGameScreen(self._application, self.__max_size)
        open_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_game_screen.play_game_signal.connect(self.__load_game_screen)
        return open_game_screen

    def __config_game_screen(self): # Initialise config game screen
        config_game_screen = ConfigGameScreen(self._application, self.__max_size)
        config_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        config_game_screen.play_game_signal.connect(self.__show_game_screen)
        return config_game_screen

    def __game_screen(self, game): # Initialise game screen
        game_screen = GameScreen(self._application, self.__max_size, game)
        game_screen.return_to_home_screen_signal.connect(self.__quit_game)
        return game_screen

    def __create_new_account_screen(self): # Initialise create new account screen
        create_new_account_screen = CreateNewAccountScreen(self._application, self.__max_size)
        create_new_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return create_new_account_screen

    def __sign_in_screen(self): # Initialise sign in screen
        sign_in_screen = SignInScreen(self._application, self.__max_size)
        sign_in_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return sign_in_screen

    def __manage_account_screen(self): # Initialise manage account screen
        manage_account_screen = ManageAccountScreen(self._application, self.__max_size)
        manage_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return manage_account_screen

    def __view_gui_presets_screen(self): # Initialise view gui presets screen
        view_gui_presets_screen = ViewGUIPresetsScreen(self._application, self.__max_size)
        view_gui_presets_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        view_gui_presets_screen.update_preset_signal.connect(self.__show_edit_gui_preset_screen)
        return view_gui_presets_screen
    
    def __edit_gui_preset_screen(self, mode, preset_id): # Initialise edit gui preset screen
        edit_gui_preset_screen = EditGUIPresetScreen(self._application, self.__max_size, mode, preset_id)
        edit_gui_preset_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return edit_gui_preset_screen
    
    def __view_stats_screen(self): # Initialise view stats screen
        view_stats_screen = ViewStatsScreen(self._application, self.__max_size)
        view_stats_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return view_stats_screen
    
    def __game_milestones_screen(self): # Initialise game milestones screen
        game_milestones_screen = GameMilestonesScreen(self._application, self.__max_size)
        game_milestones_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        #game_milestones_screen.claim_reward_signal.connect(self._application.claim_reward)
        return game_milestones_screen

    def __help_screen(self): # Initialise help screen
        help_screen = HelpScreen(self._application, self.__max_size)
        help_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return help_screen
    
    def __leaderboard_screen(self): # Initialise leaderboard screen
        leaderboard_screen = LeaderboardScreen(self._application, self.__max_size)
        leaderboard_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return leaderboard_screen

    def __close_curr_screen(self): # Close current screen method
        self.__screens[self._get_curr_ui()].close()
    
    def __show_curr_screen(self): # Show current screen method (show maximised or normal size based on options file)
        if self.__options["full screen"]:
            self.__screens[self._get_curr_ui()].initShowMaximised()
        else:
            self.__screens[self._get_curr_ui()].show()
   
    def __push_screen(self, screen): # Push screen to ui stack method
        self.__close_curr_screen()
        self._push_ui_to_stack(screen)
        self.__show_curr_screen()
        
    def __pop_screen(self): # Pop screen from ui stack method
        self.__close_curr_screen()
        self._pop_ui_from_stack()
        self.__screens[ui] = self.__screen_partials[ui := self._get_curr_ui()]()
        self.__show_curr_screen()
    
    def __show_screen(self, screen_name, screen_func): # Method to create new instance of a screen and show it
        self.__screens[screen_name] = screen_func()
        self.__push_screen(screen_name)
    
    def __show_game_screen(self, options): # Show game screen (generate new game)
        mode, difficulty, board_size, timed, hardcore = options
        self.__game = Game()
        bonus_hints = 0 if not self._application.signed_in else self._application.account.bonus_hints
        self.__game.generate(mode, difficulty, board_size, timed, hardcore, bonus_hints)
        self.__screens["game"] = self.__game_screen(self.__game)
        self.__push_screen("game")
    
    def __load_game_screen(self, file): # Load game screen (load from file)
        self.__game = Game()
        self.__game.load_game(self._application.account.username, file)
        self.__screens["game"] = self.__game_screen(self.__game)
        self.__push_screen("game")
    
    def __show_edit_gui_preset_screen(self, options):
        mode, preset_id = options
        self.__screens["edit gui preset"] = self.__edit_gui_preset_screen(mode, preset_id)
        self.__push_screen("edit gui preset")
        
    def __quit_game(self): # Quit game screen (returns to home screen)
        self.__close_curr_screen()
        while self._get_curr_ui() != "home":
            self._pop_ui_from_stack()
        self.__show_screen(self._get_curr_ui(), self.__screen_partials[self._get_curr_ui()])

    def __sign_out(self): # Method to sign out
        self._application.sign_out()
        self.__close_curr_screen()
        self.__show_screen("home", self.__screen_partials["home"])
        
    def run(self): # run function executed by sudoku.py
        exit(self.__pyqt_app.exec())
