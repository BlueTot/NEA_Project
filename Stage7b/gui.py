'''Library Imports'''

from sys import argv, exit # Import argv and edit from sys
import os # Import os module
from functools import partial # Import partial from functools module
import json # Import json module
from roman import toRoman # Import roman numerals module

'''File Imports'''

from game import Game, GameError # Import Game class and GameError exception class
from ui import UI # Import UI
from board import to_letter # Import to_letter function
import database # Import database
from database import DBError # Import Database Error
from account import * # Import account, appearance config and gme milestone classes

'''PyQt6 GUI Imports'''

from PyQt6.QtCore import QSize, Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox
from pyqt_widgets import * # Import all customisable widget classes
  
class HomeScreen(Screen):

    play_singleplayer_signal = pyqtSignal()
    create_new_account_signal = pyqtSignal()
    sign_in_singal = pyqtSignal()
    sign_out_signal = pyqtSignal()
    manage_account_signal = pyqtSignal()
    view_stats_signal = pyqtSignal()
    game_milestones_signal = pyqtSignal()
    customise_gui_signal = pyqtSignal()
    help_signal = pyqtSignal()
    leaderboard_signal = pyqtSignal()

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "S U D O K U", 0, 75, 1000, 100, self._application.account.app_config.title_font, 70)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__title.setStyleSheet("background: transparent;")

        self.__play_singleplayer_button = Button(self, "PLAY SINGLEPLAYER", 300, 250, 400, 50, self._application.account.app_config.regular_font, 25, self.__play_singleplayer)
        self.__play_singleplayer_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self.__play_multiplayer_button = Button(self, "PLAY MULTIPLAYER", 300, 320, 400, 50, self._application.account.app_config.regular_font, 25, None)
        self.__play_multiplayer_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self.__leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, self._application.account.app_config.regular_font, 25, self.__leaderboard_screen)
        self.__leaderboard_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self.__toolbar = ToolBar(self, size := QSize(60, 60), self._application.account.app_config.colour3, font_family := self._application.account.app_config.regular_font, font_size := 15)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.__toolbar)
        self.__toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.__quit_game, False))
        if self._application.account.username is None:
            options = [("Create Account", self.__create_new_account), ("Sign In", self.__sign_in)]
        else:
            options = [("Create Account", self.__create_new_account), ("Sign Out", self.__sign_out)]
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), size, QFont(font_family, font_size), options))
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), size, QFont(font_family, font_size), 
                                     [("Customise GUI", self.__customise_gui), ("Manage Account", self.__manage_account)]))
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/stats.svg"), size, QFont(font_family, font_size), [("Show Stats", self.__view_stats), ("Game Milestones", self.__game_milestones)]))
        self.__toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", self.__help_screen, False))

        self.__account_label = Label(self, "Not Signed In" if self._application.account.username is None else f"Signed in as {self._application.account.username} ({self._application.account.singleplayer_title} | {self._application.account.singleplayer_rating})", 
                                     0, 0, 400, 50, self._application.account.app_config.regular_font, 15)

        self._widgets += [self.__title, self.__play_singleplayer_button, self.__play_multiplayer_button, self.__leaderboard_button, self.__toolbar, self.__account_label]

    def __play_singleplayer(self):
        self.play_singleplayer_signal.emit()
    
    def __create_new_account(self):
        self.create_new_account_signal.emit()
    
    def __sign_in(self):
        self.sign_in_singal.emit()
    
    def __sign_out(self):
        self.sign_out_signal.emit()
    
    def __manage_account(self):
        if self._application.account.username is None:
            self.statusBar().showMessage("Please sign in to manage account")
        else:
            self.manage_account_signal.emit()
    
    def __customise_gui(self):
        if self._application.account.username is None:
            self.statusBar().showMessage("Please sign in to customise GUI")
        else:
            self.customise_gui_signal.emit()
    
    def __view_stats(self):
        if self._application.account.username is None:
            self.statusBar().showMessage("Please sign in to view stats")
        else:
            self.view_stats_signal.emit()
    
    def __game_milestones(self):
        if self._application.account.username is None:
            self.statusBar().showMessage("Please sign in to view game milestones")
        else:
            self.game_milestones_signal.emit()
    
    def __help_screen(self):
        self.help_signal.emit()

    def __leaderboard_screen(self):
        self.leaderboard_signal.emit()

    def __quit_game(self):
        exit()

class OpenOrCreateNewGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    create_new_game_signal = pyqtSignal()
    open_game_signal = pyqtSignal()

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__open_game_button = Button(self, "OPEN EXISTING GAME", 70, 80, 400, 400, self._application.account.app_config.regular_font, 25, self.__open_game)
        self.__open_game_button.setStyleSheet(f"background: {self._application.account.app_config.colour4}; border: 5px solid black;")
        self.__create_new_game_button = Button(self, "CREATE NEW GAME", 530, 80, 400, 400, self._application.account.app_config.regular_font, 25, self.__create_new_game)
        self.__create_new_game_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 5px solid black;")

        self.__back_button = BackButton(self, self.__return_to_home_screen)

        self._widgets += [self.__open_game_button, self.__create_new_game_button, self.__back_button]
    
    def __open_game(self):
        if self._application.account.username is not None:
            if os.listdir("games"):
                self.open_game_signal.emit()
            else:
                self.statusBar().showMessage("*There are no saved games at this moment, please create a new game")
        else:
                self.statusBar().showMessage("*Please sign in to an account to open saved games")

    def __create_new_game(self):
        self.create_new_game_signal.emit()

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class OpenGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    play_game_signal = pyqtSignal(str)

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "OPEN EXISTING GAME", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, self._application.account.app_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__choose_game = Label(self, "CHOOSE A GAME: ", 50, 150, 300, 100, self._application.account.app_config.regular_font, 20)
        self.__choose_game_menu = ComboBox(self, 50, 230, 400, 50,self._application.account.app_config.regular_font, 15, 
                                           os.listdir(os.path.join(Game.DEFAULT_DIRECTORY, self._application.account.username)) if self._application.account.username is not None else [])
        self.__choose_game_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__choose_game_menu.activated.connect(self.__show_game_info)

        self.__game_info = TextEdit(self, 50, 300, 400, 235, self._application.account.app_config.colour2,  2, self._application.account.app_config.regular_font, 18)

        self._widgets += [self.__title, self.__play, self.__back, self.__choose_game, self.__choose_game_menu, self.__game_info]
    
    def __show_game_info(self):
        if file := self.__choose_game_menu.currentText():
            stats = Game.get_stats_from(self._application.account.username, file)
            labels = ["Creation Date", "Creation Time", "Mode", "Difficulty", "Board Size"]
            self.__game_info.setText("\n".join([f"{label}: {stats[label.lower()]}" for label in labels]))
        else:
            self.__game_info.setText("")
            
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()
    
    def __play_game(self):
        if file := self.__choose_game_menu.currentText():
            self.play_game_signal.emit(file)
        else:
            self.statusBar().showMessage("*To continue, please select a game file to play")

class ConfigGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    play_game_signal = pyqtSignal(list)

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "CREATE NEW GAME", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, self._application.account.app_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__back = BackButton(self, self.__return_to_home_screen)

        for idx, label in enumerate(("MODE: ", "DIFFICULTY: ", "TIMED: ", "BOARD_SIZE: ", "HARDCORE: ")):
            label_obj = Label(self, label, 50, 150+75*idx, 300, 100, self._application.account.app_config.regular_font, 24)
            self._widgets.append(label_obj)

        self.__mode_menu = ComboBox(self, 330, 175, 200, 50, self._application.account.app_config.regular_font, 20, ["Normal", "Killer"])
        self.__mode_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__difficulty_menu = ComboBox(self, 330, 250, 200, 50, self._application.account.app_config.regular_font, 20, ["Easy", "Medium", "Hard", "Expert"])
        self.__difficulty_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__timed_menu = ComboBox(self, 330, 325, 200, 50, self._application.account.app_config.regular_font, 20, ["Yes", "No"])
        self.__timed_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__board_size_menu = ComboBox(self, 330, 400, 200, 50, self._application.account.app_config.regular_font, 20, ["4x4", "6x6", "9x9", "12x12", "16x16"])
        self.__board_size_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__hardcore_menu = ComboBox(self, 330, 475, 200, 50, self._application.account.app_config.regular_font, 20, ["Yes", "No"])
        self.__hardcore_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__play, self.__back, self.__mode_menu, self.__difficulty_menu, 
                          self.__timed_menu, self.__board_size_menu, self.__hardcore_menu]

    def __play_game(self):
        if (difficulty := self.__difficulty_menu.currentText()) and (timed := self.__timed_menu.currentText()) and \
            (board_size := self.__board_size_menu.currentText()) and (mode := self.__mode_menu.currentText()) and \
                (hardcore := self.__hardcore_menu.currentText()):
            if board_size == "16x16" and difficulty == "Expert":
                self.statusBar().showMessage("*16x16 Expert is not available")
            elif board_size == "16x16" and difficulty == "Hard":
                self.statusBar().showMessage("*16x16 Hard is not available")
            else:
                self.setWindowTitle("Board Generation in Progress")
                self.play_game_signal.emit([mode, difficulty, int(board_size.split("x")[0]), True if timed == "Yes" else False, True if hardcore == "Yes" else False])
        else:
            self.statusBar().showMessage("*To continue, please fill all boxes")

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    save_stats_signal = pyqtSignal(list)
    update_rating_signal = pyqtSignal(int)
    update_milestone_signal = pyqtSignal(list)
    PADDING, STARTX = 25, 10
    NUM_FONT_SIZES = {4: 20*9 // 4, 6: 20*9 // 6, 9: 20, 12: 20 * 9 // 12, 16: 20*9 // 16}
    HINT_FONT_SIZES = {4: 13*9 // 4, 6: 13*9 // 6, 9: 13, 12: 13 * 9 // 12, 16: 5}
    TOTAL_FONT_SIZES = {4: 10*9 // 4, 6: 10*9 // 6, 9: 10, 12: 10 * 9 // 12, 16: 10 * 9 // 16}

    def __init__(self, application, max_size):
        
        super().__init__(application, max_size)

        self.__selected_square = (None, None)
        self.__notes_mode = False
        self.__running = True

        self.__timer = Button(self, "", 610, 20, 130, 65, self._application.account.app_config.regular_font, 21, self.__pause_game)
        self.__timer.setStyleSheet("border: 2px solid black;")
        self.__progress = ProgressBar(self, 610, 110, 330, 20)
        self.__progress.setStyleSheet("QProgressBar::chunk{background-color: " + self._application.account.app_config.colour2 + ";}")

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.__info_label = Label(self, "", 595, 15, 310, 90, self._application.account.app_config.regular_font, 12)
        self.__info_label.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black; border-radius: 30px;")
        self.__info_label.hide()
        self.__info_button = CircularButton(self, 845, 15, 60, 60, QIcon("resources/info.svg"), self.__toggle_info_screen)

        self.__undo_button = CircularButton(self, 610, 470, 58, 58, QIcon("resources/undo.svg"), self.__undo_move)
        self.__auto_note_button = CircularButton(self, 677, 470, 58, 58, QIcon("resources/auto_note.svg"), self.__show_auto_note)
        self.__num_auto_notes_label = Label(self, "", 681, 535, 58, 58, self._application.account.app_config.regular_font, 15)
        self.__num_auto_notes_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__hint_button = CircularButton(self, 744, 470, 58, 58, QIcon("resources/hint.svg"), self.__show_hint)
        self.__num_hints_label = Label(self, "", 748, 535, 58, 58, self._application.account.app_config.regular_font, 15)
        self.__num_hints_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__notes_button = CircularButton(self, 811, 470, 58, 58, QIcon("resources/notes_off.svg"), self.__toggle_notes_mode)
        self.__notes_button.setIconSize(QSize(53, 53))
        self.__notes_button.setStyleSheet("border-radius: 29px; border: 5px solid black;")
        self.__resign_button = CircularButton(self, 878, 470, 58, 58, QIcon("resources/resign.svg"), partial(self.__show_end_screen, False))

        self._widgets += [self.__timer, self.__back, self.__info_label, self.__info_button, self.__undo_button, 
                          self.__auto_note_button, self.__hint_button, self.__num_auto_notes_label, self.__num_hints_label, self.__notes_button, 
                          self.__resign_button, self.__progress]

    def __show_border(self, board_size, matrix_size):

        big_border = Border(self, self.STARTX+self.PADDING-3, self.PADDING-3, 
                            self.GRIDSIZE*board_size+6+6, self.GRIDSIZE*board_size+6+6, 3)
        big_border.show()
        self._widgets.append(big_border)
        for row in range(matrix_size[1]):
            for col in range(matrix_size[0]):
                border = Border(self, self.STARTX + self.PADDING + self.GRIDSIZE*matrix_size[1]*col + 3*col, 
                                self.PADDING + self.GRIDSIZE*matrix_size[0]*row + 3*row, 
                                self.GRIDSIZE*matrix_size[1]+3, self.GRIDSIZE*matrix_size[0]+3, 3)
                border.show()
                self._widgets.append(border)

    def set_game(self, game : Game):

        self.__game = game
        self.__info_label.setText(f"Mode: {self.__game.mode} \nDifficulty: {self.__game.difficulty} \nBoard Size: {self.__game.board_size}x{self.__game.board_size} \nTimed: {self.__game.timed} \nHardcore: {self.__game.hardcore}")
        self.__num_auto_notes_label.setText(f"{self.__game.num_auto_notes_left}")
        if self._application.account.username is None:
            bonus_hint_str = ""
        else:
            bonus_hint_str = f'(+{bonus_hints})' if (bonus_hints := database.bonus_hints(self._application.account.username)) != 0 and self.__game.num_hints_left > 0 else ''
        self.__num_hints_label.setText(f"{self.__game.num_hints_left} {bonus_hint_str}")

        if self.__game.mode == "Killer":
            self.__colours = self.__game.group_colours

        self.__create_curr_grid()
        self.__progress.setValue(int(self.__game.percent_complete()))

        self.__board_cover = Rect(self, self.STARTX+self.PADDING-3, self.PADDING-3, width:= self.GRIDSIZE*self.__game.board_size+12, height := self.GRIDSIZE*self.__game.board_size+12,
                                  self._application.account.app_config.colour2, 5)

        self.__paused_label = Label(self.__board_cover, "GAME PAUSED", 0, 0, width, height, self._application.account.app_config.regular_font, 24)
        self.__paused_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__board_cover.hide()

        self._widgets += [self.__paused_label, self.__board_cover]

        if self.__game.timed:
            self.__timer_event = QTimer()
            self.__timer_event.timeout.connect(self.__update_time_elapsed)
            self.__timer_event.start(10)
        else:
            self.__timer.setText("---")

    def __create_number_grid(self, curr_board, orig_board):

        BOARD_SIZE, MATRIX_SIZE = self.__game.board_size, self.__game.matrix_size
        self.GRIDSIZE = (560 - 2 * self.PADDING) // BOARD_SIZE

        self.__show_border(BOARD_SIZE, MATRIX_SIZE)

        NUM_INP_SIZE = (330 // MATRIX_SIZE[1], 330 // MATRIX_SIZE[0])
        STARTX, STARTY = 610, 130
        for ridx in range(MATRIX_SIZE[1]):
            for cidx in range(MATRIX_SIZE[0]):
                num_input = Button(self, num := to_letter(ridx*MATRIX_SIZE[0]+cidx+1), STARTX+NUM_INP_SIZE[1]*cidx, STARTY+NUM_INP_SIZE[0]*ridx, NUM_INP_SIZE[1], NUM_INP_SIZE[0], 
                                   self._application.account.app_config.regular_font, 20, partial(self.__place_num, num))
                num_input.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
                self._widgets.append(num_input)

        self.__sqrs = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.__num_font_size, self.__hint_font_size, self.__total_font_size = self.NUM_FONT_SIZES[BOARD_SIZE], self.HINT_FONT_SIZES[BOARD_SIZE], self.TOTAL_FONT_SIZES[BOARD_SIZE]
    
        for row, row_lst in enumerate(curr_board):
            for col, sq in enumerate(row_lst):
                square = Button(window = self, 
                                text = num if (num := to_letter(sq.num)) != "0" else self.__game.note_at(row, col),
                                x = self.STARTX + self.PADDING + self.GRIDSIZE*col + MATRIX_SIZE[1]*(col//MATRIX_SIZE[1]),
                                y = self.PADDING + self.GRIDSIZE*row + MATRIX_SIZE[0]*(row//MATRIX_SIZE[0]), 
                                width = self.GRIDSIZE, 
                                height = self.GRIDSIZE, 
                                font_family = self._application.account.app_config.regular_font,
                                font_size = self.__num_font_size if sq.num != 0 else self.__hint_font_size, 
                                command = partial(self.__select_square, row+1, col+1))
                square.setFont(QFont(self._application.account.app_config.regular_font, self.__num_font_size if sq.num != 0 else self.__hint_font_size))
                square.setStyleSheet(f"border: {5 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + 
                                     ((self._application.account.app_config.colour2 if self.__game.mode == "Normal" else "#C8C8C8") if (row+1, col+1) == self.__selected_square else ("white" if self.__game.mode == 'Normal' else self._application.account.app_config.killer_colours[self.__colours[(row, col)]])) + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if sq.num != 0 else "red")) + 
                                     (";text-align: left" if sq.num == 0 else "") + 
                                     ";")
                self.__sqrs[row][col] = square
                self._widgets.append(square)
                square.show()  

                if self.__game.mode == "Killer" and (row, col) in self.__game.groups:
                    total_label = Label(self, str(self.__game.groups[(row, col)][1]), square.x(), square.y(), square.width()//3, square.height()//3, self._application.account.app_config.regular_font, self.__total_font_size)
                    total_label.setStyleSheet("background: transparent;")
                    total_label.show()
                    self._widgets.append(total_label)

    def __update_number_grid(self, curr_board, orig_board):
        mult = self._resize_factor if self.isMaximized() else 1
        for row, row_lst in enumerate(self.__sqrs):
            for col, sq in enumerate(row_lst):
                sq.setText(str(num) if (num := to_letter(curr_board[row][col].num)) != "0" else self.__game.note_at(row, col))
                sq.setFont(QFont(self._application.account.app_config.regular_font, int(mult * (self.__num_font_size if num != "0" else self.__hint_font_size))))
                sq.setStyleSheet(f"border: {3 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + 
                                     ((self._application.account.app_config.colour2 if self.__game.mode == "Normal" else "#C8C8C8") if (row+1, col+1) == self.__selected_square else ("white" if self.__game.mode == 'Normal' else self._application.account.app_config.killer_colours[self.__colours[(row, col)]])) + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if num != "0" else "red")) + 
                                     (";text-align: left" if num == "0" else "") + 
                                     ";")
        self.__progress.setValue(int(self.__game.percent_complete()))
    
    def __create_curr_grid(self):
        self.__create_number_grid(self.__game.curr_board, self.__game.orig_board)
    
    def __update_curr_grid(self):
        self.__update_number_grid(self.__game.curr_board, self.__game.orig_board)
    
    def __create_solution_grid(self):
        self.__create_number_grid(self.__game.solved_board, self.__game.orig_board)
    
    def __show_end_screen(self, win):

        self.__running = False
        self.__selected_square = (None, None)
        self.__game.remove_game_file(self._application.account.username)
        if self.__game.timed:
            self.__timer_event.stop()
        if self._application.account.username is not None and self.__game.timed:
            self.save_stats_signal.emit(self.__game.get_stats(win))
            self.update_rating_signal.emit(rating_change := self.__game.rating_change(self._application.account.singleplayer_rating, win))
            self.update_milestone_signal.emit([self.__game.mode, self.__game.board_size, self.__game.difficulty, win])

        bg = Rect(self, 0, 0, 1000, 560, self._application.account.app_config.colour2_translucent, 0)
        bg.show()

        window = Rect(self, 200, 30, 600, 500, "white", 5)
        window.show()
    
        title = Label(self, "You Won!" if win else "Game Over!", 0, 50, 1000, 100, self._application.account.app_config.title_font, 40)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("background: transparent;")
        title.show()

        if self.__game.timed:

            time_label_top = Label(self, "Time Elapsed: ", 0, 140, 1000, 100, self._application.account.app_config.regular_font, 20)
            time_label_top.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time_label_top.setStyleSheet("background: transparent;")
            time_label_top.show()

            time = Label(self, self.__game.time_elapsed, 0, 180, 1000, 100, self._application.account.app_config.regular_font, 60)
            time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time.setStyleSheet("background: transparent;")
            time.show()

            if self._application.account.username is not None:

                rating_label_top = Label(self, "New Rating: ", 0, 270, 1000, 100, self._application.account.app_config.regular_font, 20)
                rating_label_top.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating_label_top.setStyleSheet("background: transparent;")
                rating_label_top.show()

                rating = Label(self, rating_str := str(self._application.account.singleplayer_rating), 0, 310, 1000, 100, self._application.account.app_config.regular_font, 60)
                rating.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating.setStyleSheet("background: transparent;")
                rating.show()

                rating_change = Label(self, f"({f'+{rating_change}' if rating_change >= 0 else rating_change})", 60*len(rating_str), 350, 1000, 100, self._application.account.app_config.regular_font, 20)
                rating_change.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                rating_change.setStyleSheet("background: transparent;")
                rating_change.show()

                self._widgets += [rating_label_top, rating, rating_change]
            
            self._widgets += [time, time_label_top]

        home_screen_button = Button(self, "RETURN TO HOME", 350, 450, 300, 50, self._application.account.app_config.regular_font, 20, self.__return_to_home_screen)
        home_screen_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        home_screen_button.show()

        solution_button = Button(self, "SEE SOLUTION", 350, 390, 300, 50, self._application.account.app_config.regular_font, 20,self.__show_solution_screen)
        solution_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        if not win:
            solution_button.show()
        
        self._widgets += [bg, window, title, home_screen_button, solution_button]

        self.manualMaximise()
    
    def __show_solution_screen(self):

        bg = Rect(self, 0, 0, 1000, 560, "white", 0)
        bg.show()
        
        self.__show_border(self.__game.board_size, self.__game.matrix_size)
        self.__create_solution_grid()

        home_screen_button = Button(self, "RETURN TO HOME", 625, 250, 300, 50, self._application.account.app_config.regular_font, 20, self.__return_to_home_screen)
        home_screen_button.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        home_screen_button.show()
        
        self._widgets += [bg, home_screen_button]

        self.manualMaximise()
    
    def __show_game_paused_error(self):
        self.statusBar().showMessage("ERROR: This action cannot be performed while the game is paused")

    def __select_square(self, row, col):
        if self.__running:
            self.__selected_square = (row, col)
            self.__update_curr_grid()

    def __place_num(self, num):
        if self.__running:
            try:
                if self.__notes_mode:
                    self.__game.edit_note(self.__selected_square[0], self.__selected_square[1], num)
                else:
                    if self.__game.get_num_at(self.__selected_square[0], self.__selected_square[1]) == 0:
                        self.__game.put_down_number(self.__selected_square[0], self.__selected_square[1], num)   
                    else:
                        self.__game.remove_number(self.__selected_square[0], self.__selected_square[1])         
            except GameError as err:
                self.show_error(err)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
        if self.__game.is_complete():
            self.__show_end_screen(True)
    
    def __show_auto_note(self):
        if self.__running:
            try:
                self.__game.use_auto_note(self.__selected_square[0], self.__selected_square[1])
                self.__num_auto_notes_label.setText(str(self.__game.num_auto_notes_left))
            except GameError as err:
                self.show_error(err)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
    
    def __show_hint(self):
        if self.__running:
            try:
                self.__game.use_hint(self.__selected_square[0], self.__selected_square[1])
                if self._application.account.username is None:
                    bonus_hint_str = ""
                else:
                    bonus_hint_str = f'(+{bonus_hints})' if (bonus_hints := database.bonus_hints(self._application.account.username)) != 0 and self.__game.num_hints_left > 0 else ''
                self.__num_hints_label.setText(f"{self.__game.num_hints_left} {bonus_hint_str}")
            except GameError as err:
                self.show_error(err)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
    
    def __toggle_notes_mode(self):
        if self.__running:
            self.__notes_mode = not self.__notes_mode
            self.__notes_button.setIcon(QIcon("resources/notes_on.svg" if self.__notes_mode else "resources/notes_off.svg"))
        else:
            self.__show_game_paused_error()
    
    def __undo_move(self):
        if self.__running:
            self.__game.undo_last_move()
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
    
    def __toggle_info_screen(self):
        self.__info_label.setHidden(not self.__info_label.isHidden())
    
    def __pause_game(self):
        self.__running = not self.__running
        self.__timer.setStyleSheet(f"background: {'white' if self.__running else self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__board_cover.setHidden(not self.__board_cover.isHidden())
        if self.__game.timed:
            if self.__running: self.__timer_event.start(10)
            else: self.__timer_event.stop()
    
    def __update_time_elapsed(self):
        self.__game.inc_time_elapsed()
        self.__timer.setText(str(self.__game.time_elapsed))

    def __return_to_home_screen(self):
        if self.__running and self._application.account.username is not None: # game quit from the "back" button
            self.__game.save_game(self._application.account.username)
        self.return_to_home_screen_signal.emit()

class CreateNewAccountScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    create_account_signal = pyqtSignal(list)
    
    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "CREATE NEW ACCOUNT", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._application.account.app_config.regular_font, 20)

        self.__password = LineEdit(self, 400, 300, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._application.account.app_config.regular_font, 20)

        self.__password2 = LineEdit(self, 400, 400, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label2 = Label(self, "Enter password again: ", 100, 400, 300, 50, self._application.account.app_config.regular_font, 20)

        self.__create = Button(self, "Create", 400, 500, 200, 50, self._application.account.app_config.regular_font, 20, self.__create_account)
        self.__create.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__back, self.__username, self.__username_label, self.__password, 
                          self.__password_label, self.__password2, self.__password_label2, self.__create]

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()
    
    def __create_account(self):
        if self.__username.text() and self.__password.text() and self.__password2.text():
            if self.__password.text() == self.__password2.text():
                self.create_account_signal.emit([self.__username.text(), self.__password.text()])
            else:
                self.statusBar().showMessage("Passwords inputted are not the same")
        else:
            self.statusBar().showMessage("One or more input boxes are still empty")

class SignInScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    sign_in_signal = pyqtSignal(list)
    
    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "SIGN IN", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._application.account.app_config.regular_font, 20)

        self.__password = LineEdit(self, 400, 300, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._application.account.app_config.regular_font, 20)

        self.__sign_in = Button(self, "Sign In", 400, 400, 200, 50, self._application.account.app_config.regular_font, 20, self.__sign_in)
        self.__sign_in.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__back, self.__username, self.__username_label, self.__password, 
                          self.__password_label, self.__sign_in]
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()
    
    def __sign_in(self):
        if self.__username.text() and self.__password.text():
            self.sign_in_signal.emit([self.__username.text(), self.__password.text()])
        else:
            self.statusBar().showMessage("One or more input boxes are still empty")

class ViewGUIPresetsScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    update_preset_signal = pyqtSignal(list)
    use_preset_signal = pyqtSignal(int)

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "VIEW PRESETS", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__create_preset = Button(self, "CREATE PRESET", 600, 180, 300, 100, self._application.account.app_config.regular_font, 22, self.__create_preset)
        self.__create_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;")
        self.__edit_preset = Button(self, "EDIT PRESET", 600, 310, 300, 100, self._application.account.app_config.regular_font, 22, self.__edit_preset)
        self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")
        self.__use_preset = Button(self, "USE PRESET", 600, 440, 300, 100, self._application.account.app_config.regular_font, 22, self.__use_preset)
        self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")

        self.__current_preset = Label(self, f"CURRENT PRESET: Preset {database.get_current_appearance_preset_num(self._application.account.username)}", 50, 150, 400, 60, self._application.account.app_config.regular_font, 20)
        self.__choose_preset = Label(self, "CHOOSE A PRESET", 50, 200, 300, 50, self._application.account.app_config.regular_font, 20)
        self.__choose_preset_menu = ComboBox(self, 50, 245, 400, 50,self._application.account.app_config.regular_font, 15, 
                                           [f"Preset {preset[0]}" for preset in database.get_all_presets(self._application.account.username)])
        self.__choose_preset_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__choose_preset_menu.activated.connect(self.__show_preset_info)

        self.__preset_preview = TextEdit(self, 50, 325, 400, 235, self._application.account.app_config.colour2, 2, self._application.account.app_config.regular_font, 14)

        self._widgets += [self.__title, self.__back, self.__choose_preset, self.__choose_preset_menu, 
                          self.__create_preset, self.__edit_preset, self.__use_preset, self.__preset_preview,
                          self.__current_preset]
    
    def __create_preset(self):
        self.update_preset_signal.emit(["create", database.next_preset_number(self._application.account.username)])

    def __edit_preset(self):
        if (text := self.__choose_preset_menu.currentText()):
            if (text := self.__choose_preset_menu.currentText()) != "Preset 1":
                self.update_preset_signal.emit(["edit", int(text.split(" ")[1])])
            else:
                self.statusBar().showMessage("*Preset 1 is the default appearance present and cannot be edited.")
        else:
            self.statusBar().showMessage("*Please select a preset to edit")
    
    def __use_preset(self):
        if (text := self.__choose_preset_menu.currentText()):
            if database.get_current_appearance_preset_num(self._application.account.username) != (num := int(text.split(" ")[1])):
                self.use_preset_signal.emit(num)
                self.__current_preset.setText(f"CURRENT PRESET: Preset {database.get_current_appearance_preset_num(self._application.account.username)}")
            else:
                self.statusBar().showMessage(f"*Preset {num} is currently being used.") 
        else:
            self.statusBar().showMessage("*Please select a preset to use")
        
    def __show_preset_info(self):
        if (text := self.__choose_preset_menu.currentText()):
            self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;")
            self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3]}; border: 2px solid black;")
            data = database.get_preset(self._application.account.username, int(text.split(" ")[1]))
            labels = ["Background Colour", "Colour 1", "Colour 2", "Colour 3", "Colour 4", "Title Font",
                      "Regular Font", "Killer Colour 1", "Killer Colour 2", "Killer Colour 3", "Killer Colour 4", "Killer Colour 5"]
            self.__preset_preview.setText("\n".join([f"{label}: {stat}" for label, stat in zip(labels, data)]))
        else:
            self.__edit_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")
            self.__use_preset.setStyleSheet(f"background: {self._application.account.app_config.colour3}; border: 2px solid black;")
            self.__preset_preview.setText("")

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class EditGUIPresetScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    save_signal = pyqtSignal(list)
    delete_signal = pyqtSignal(int)

    def __init__(self, application, max_size, mode, preset_num):

        super().__init__(application, max_size)

        self.__mode = mode
        self.__preset_num = preset_num

        try:
            self.__curr_preset = database.get_preset(self._application.account.username, preset_num)
        except IndexError:
            self.__curr_preset = database.get_preset(self._application.account.username, 1)
        
        self.__title = Label(self, f"{'EDIT' if mode == 'edit' else 'CREATE'} PRESET {preset_num}", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        for idx, label in enumerate(("Background Colour", "Colour 1", "Colour 2", "Colour 3", "Colour 4", "Title Font")):
            label_obj = Label(self, label, 50, 150+60*idx, 300, 40, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)
        
        for idx, label in enumerate(("Regular Font", "Killer Colour 1", "Killer Colour 2", "Killer Colour 3", "Killer Colour 4", "Killer Colour 5")):
            label_obj = Label(self, label, 575, 150+60*idx, 300, 40, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)
        
        self.__bg_colour = LineEdit(self, 325, 150, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[0], False)
        self.__colour1 = LineEdit(self, 325, 210, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[1], False)
        self.__colour2 = LineEdit(self, 325, 270, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[2], False)
        self.__colour3 = LineEdit(self, 325, 330, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[3], False)
        self.__colour4 = LineEdit(self, 325, 390, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[4], False)

        self.__title_font = ComboBox(self, 325, 450, 200, 50, self._application.account.app_config.regular_font, 14, QFontDatabase.families(), add_blank=False)
        self.__title_font.setCurrentText(self.__curr_preset[5])
        self.__title_font.setStyleSheet(f"background: white; border: 2px solid black;")

        self.__regular_font = ComboBox(self, 775, 150, 200, 50, self._application.account.app_config.regular_font, 14, QFontDatabase.families(), add_blank=False)
        self.__regular_font.setCurrentText(self.__curr_preset[6])
        self.__regular_font.setStyleSheet(f"background: white; border: 2px solid black;")

        self.__killer_colour1 = LineEdit(self, 775, 210, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[7], False)
        self.__killer_colour2 = LineEdit(self, 775, 270, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[8], False)
        self.__killer_colour3 = LineEdit(self, 775, 330, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[9], False)
        self.__killer_colour4 = LineEdit(self, 775, 390, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[10], False)
        self.__killer_colour5 = LineEdit(self, 775, 450, 120, 50, self._application.account.app_config.regular_font, 14, self.__curr_preset[11], False)

        self.__options = [self.__bg_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__killer_colour1, 
                          self.__killer_colour2, self.__killer_colour3, self.__killer_colour4, self.__killer_colour5]

        self.__save = Button(self, "Save Changes", 275, 525, 200, 50, self._application.account.app_config.regular_font, 18, self.__save)
        self.__save.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self.__delete = Button(self, "Delete Preset", 525, 525, 200, 50, self._application.account.app_config.regular_font, 18, self.__delete)
        self.__delete.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__back, self.__bg_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__title_font, 
                          self.__regular_font, self.__killer_colour1, self.__killer_colour2, self.__killer_colour3, self.__killer_colour4, self.__killer_colour5,
                          self.__save, self.__delete]
    
    def __get_options(self):
        options = [text if (text := textbox.text()) else textbox.placeholderText() for textbox in self.__options]
        combo_boxes = [self.__title_font.currentText(), self.__regular_font.currentText()]
        return options[0:5] + combo_boxes + options[5:]
    
    def __font_options_changed(self):
        return self.__title_font.currentText() != AppearanceConfiguration.DEFAULT_SETTINGS[5] or self.__regular_font.currentText() != AppearanceConfiguration.DEFAULT_SETTINGS[6]
    
    def __save(self):
        options = self.__get_options()
        if any([textbox.text() for textbox in self.__options]) or self.__font_options_changed():
            self.save_signal.emit([self.__mode, self.__preset_num] + options)
            self.__return_to_home_screen()
        else:
            self.statusBar().showMessage("Please fill in at least one box to save")
    
    def __delete(self):
        if database.get_current_appearance_preset_num(self._application.account.username) == self.__preset_num:
            self.statusBar().showMessage("*Preset is currently in use and cannot be deleted.")
        else:
            self.delete_signal.emit(self.__preset_num)
            self.__return_to_home_screen()

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class ManageAccountScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    change_username_signal = pyqtSignal(str)
    change_password_signal = pyqtSignal(str)
    delete_account_signal = pyqtSignal()
    
    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "MANAGE ACCOUNT", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        for idx, label in enumerate(("Change Username", "Old Password", "New Password", "New Password Again")):
            label_obj = Label(self, label, 100, 200+75*idx, 300, 50, self._application.account.app_config.regular_font, 18)
            self._widgets.append(label_obj)

        self.__username = LineEdit(self, 400, 200, 500, 50, self._application.account.app_config.regular_font, 15, f"Current username: {self._application.account.username}", False)
        self.__old_password = LineEdit(self, 400, 275, 500, 50, self._application.account.app_config.regular_font, 15, "**************", True)
        self.__new_password = LineEdit(self, 400, 350, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__new_password2 = LineEdit(self, 400, 425, 500, 50, self._application.account.app_config.regular_font, 15, "Type here: ", True)
        self.__textboxes = [self.__username, self.__old_password, self.__new_password, self.__new_password2]

        self.__save = Button(self, "Save Changes", 275, 500, 200, 50, self._application.account.app_config.regular_font, 18, self.__save)
        self.__save.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")

        self.__delete = Button(self, "Delete Account", 525, 500, 200, 50, self._application.account.app_config.regular_font, 18, self.__delete)
        self.__delete.setStyleSheet(f"background: {self._application.account.app_config.colour4}; border: 2px solid black;")

        self._widgets += [self.__back, self.__title, self.__username, self.__old_password, self.__new_password, 
                          self.__new_password2, self.__save, self.__delete]
    
    def __save(self):
        if any([textbox.text() for textbox in self.__textboxes]):
            if (username := self.__username.text()):
                self.change_username_signal.emit(username)
                self.__return_to_home_screen()
            if all([textbox.text() for textbox in self.__textboxes[1:]]):
                if database.encrypt_password(self.__old_password.text()) == database.password_at(self._application.account.username)[0][0]:
                    if self.__new_password.text() == self.__new_password2.text():
                        if self.__new_password.text() != self.__old_password.text():
                            self.change_password_signal.emit(self.__new_password.text())
                            self.__return_to_home_screen()
                        else:
                            self.statusBar().showMessage("Please choose a different password to your current one")
                    else:
                        self.statusBar().showMessage("New passwords inputted are not the same")
                else:
                    self.statusBar().showMessage("Incorrect original password")
            else:
                self.statusBar().showMessage("To change your password, please fill in the last 3 blanks")    
        else:
            self.statusBar().showMessage("Please either change your username or password to save")

    def __delete(self):
        self.__message_box = QMessageBox(self)
        self.__message_box.setWindowTitle("Delete Account Menu")
        self.__message_box.setText("Are you sure you want to delete your account?")
        self.__message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.__message_box.buttonClicked.connect(self.__delete_menu_button)
        self.__message_box.show()
    
    def __delete_menu_button(self, button):
        if button.text()[1:] == "Yes":
            self.delete_account_signal.emit()
            self.__return_to_home_screen()
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class ViewStatsScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    
    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "PLAYER STATS", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.__stats = TextEdit(self, 50, 150, 400, 450, self._application.account.app_config.colour2_translucent, 4, self._application.account.app_config.regular_font, 18)

        total_games = database.num_of_games(self._application.account.username)
        completed_games = database.num_completed_games(self._application.account.username)

        stats_txt = "\n".join([
        "OVERALL STATS: \n",
        f"Rating: {self._application.account.singleplayer_rating}",                         
        f"Title: {self._application.account.singleplayer_title}\n",
        f"Total Games Played: {total_games}",
        f"Completed Games: {completed_games}",
        f"% Complete: {f'{round(completed_games/total_games*100)}%' if total_games != 0 else 'N/A'}\n",
        f"Num of Bonus Hints: {database.bonus_hints(self._application.account.username)}"
        ])
    
        self.__stats.insertPlainText(stats_txt)

        for idx, label in enumerate(["Mode", "Board Size", "Difficulty"]):
            label_obj = Label(self, label, 525, 150+idx*60, 200, 45, self._application.account.app_config.regular_font, 20)
            self._widgets.append(label_obj)

        self.__mode_menu = ComboBox(self, 700, 150, 200, 45, self._application.account.app_config.regular_font, 20, ["Normal", "Killer"])
        self.__mode_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__mode_menu.activated.connect(self.update_gamemode_stats)
        self.__board_size_menu = ComboBox(self, 700, 210, 200, 45, self._application.account.app_config.regular_font, 20, ["4x4", "6x6", "9x9", "12x12", "16x16"])
        self.__board_size_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__board_size_menu.activated.connect(self.update_gamemode_stats)
        self.__difficulty_menu = ComboBox(self, 700, 270, 200, 45, self._application.account.app_config.regular_font, 20, ["Easy", "Medium", "Hard", "Expert"])
        self.__difficulty_menu.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__difficulty_menu.activated.connect(self.update_gamemode_stats)

        self.__gamemode_stats = TextEdit(self, 525, 350, 400, 250, self._application.account.app_config.colour2_translucent, 4, self._application.account.app_config.regular_font, 18)
    
        self.__back = BackButton(self, self.__return_to_home_screen)

        self._widgets += [self.__back, self.__title, self.__stats, self.__mode_menu, self.__board_size_menu, 
                          self.__difficulty_menu, self.__gamemode_stats]
    
    def update_gamemode_stats(self):
        if self.__mode_menu.currentText() and self.__board_size_menu.currentText() and self.__difficulty_menu.currentText():
            mode, board_size, difficulty = self.__mode_menu.currentText(), int(self.__board_size_menu.currentText().split("x")[0]), self.__difficulty_menu.currentText()
            self.__gamemode_stats.setText("\n".join([
                f"Times Played: {database.times_played(self._application.account.username, mode, board_size, difficulty)}",
                f"Number of Completions: {database.num_completions(self._application.account.username, mode, board_size, difficulty)}",
                f"Best Time: {database.best_time(self._application.account.username, mode, board_size, difficulty)}",
                f"Best Hardcore Time: {database.best_hardcore_time(self._application.account.username, mode, board_size, difficulty)}"
            ]))
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameMilestonesScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    claim_reward_signal = pyqtSignal(list)
    
    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "GAME MILESTONES", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__selected_milestone = None

        for idx, label in enumerate(milestone_types := ("4x4", "6x6", "9x9", "12x12", "16x16")):
            label = Label(self, label, 50, 175+80*idx, 100, 50, self._application.account.app_config.regular_font, 30)
            self._widgets.append(label)

        milestone_claimed = database.milestone_claimed(self._application.account.username)
        self.__milestone_buttons = {}
        for vidx, board_size in enumerate(milestone_types):
            for hidx, milestone_num in enumerate(range(1, 8)):
                box = Button(self, toRoman(milestone_num), x := 200+hidx*70, y := 175+80*vidx, 60, 60, self._application.account.app_config.title_font, 22, partial(self.__view_game_milestone, board_size, milestone_num))
                box.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) else 'rgb(175, 175, 175)'}; border: 3px solid black;")
                unclaimed_label = Label(self, "!" if int(milestone_claimed[vidx*7+hidx]) else "", x+48, y+5, 14, 14, self._application.account.app_config.regular_font, 14)
                unclaimed_label.setStyleSheet("background: transparent; color: red;")
                self.__milestone_buttons[(vidx, hidx)] = (board_size, milestone_num, box, unclaimed_label)
                self._widgets.extend([box, unclaimed_label])
            
        self.__milestone_data_box = TextEdit(self, 725, 175, 250, 330, self._application.account.app_config.colour2_translucent, 3, self._application.account.app_config.regular_font, 16)
        self.__claim_reward = Button(self, "Claim Reward", 725, 515, 250, 40, self._application.account.app_config.regular_font, 18, self.__claim_reward)
        self.__claim_reward.setStyleSheet("background: rgb(175, 175, 175); border: 2px solid black;")
            
        self._widgets += [self.__back, self.__title, self.__milestone_data_box, self.__claim_reward]
    
    def __update_milestone_grid(self):
        milestone_claimed = database.milestone_claimed(self._application.account.username)
        for k, v in self.__milestone_buttons.items():
            vidx, hidx = k
            board_size, milestone_num, box, unclaimed_label = v
            box.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) else 'rgb(175, 175, 175)'}; border: 3px solid black;")
            unclaimed_label.setText("!" if int(milestone_claimed[vidx*7+hidx]) else "")
        self.__view_game_milestone(self.__selected_milestone[0], self.__selected_milestone[1])

    def __complete(self, board_size, milestone_num):
        milestone = database.milestone(self._application.account.username, f"milestone_{board_size}")
        return milestone >= GameMilestones.MILESTONES[int(milestone_num)]
    
    def __parse_reward(self, reward):
        if reward is None:
            return "None"
        elif reward[0] == "H":
            return f"+{reward[1]} Hint(s)"
    
    def __selected_milestone_not_claimed(self):
        board_size, milestone_num = self.__selected_milestone
        claimed = database.milestone_claimed(self._application.account.username)
        idx = GameMilestones.BOARD_SIZE_IDXS[int(board_size.split("x")[0])] * 7 + int(milestone_num) - 1
        return int(claimed[idx])
    
    def __view_game_milestone(self, board_size, milestone_num):
        self.__selected_milestone = (board_size, milestone_num)
        milestone = database.milestone(self._application.account.username, f"milestone_{board_size}")
        status = "Complete" if self.__complete(board_size, milestone_num) else "Incomplete"
        target = GameMilestones.MILESTONES[int(milestone_num)]
        self.__milestone_data_box.setText("\n".join([
            f"{board_size} MILESTONE {toRoman(milestone_num)}: \n",
            f"Status: {status}",
            f"Progress: {milestone}/{target} ({round(milestone/target*100)}%)\n",
            f"Reward: {self.__parse_reward(GameMilestones.REWARDS[board_size][int(milestone_num)])}"
        ]))
        self.__claim_reward.setStyleSheet(f"background: {self._application.account.app_config.killer_colours[3] if self.__complete(board_size, milestone_num) else 'rgb(175, 175, 175)'}; border: 3px solid black;")
    
    def __claim_reward(self):
        if self.__selected_milestone is not None:
            if self.__complete(self.__selected_milestone[0], self.__selected_milestone[1]):
                if self.__selected_milestone_not_claimed():
                    self.claim_reward_signal.emit([int(self.__selected_milestone[0].split("x")[0]), int(self.__selected_milestone[1])])
                    self.__update_milestone_grid()
                else:
                    self.statusBar().showMessage("You already claimed this reward!")
            else:
                self.statusBar().showMessage("You haven't unlocked this reward yet!")
        else:
            self.statusBar().showMessage("Please select a milestone to claim")
        
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class HelpScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.setStyleSheet(f"background: {self._application.account.app_config.colour3};")

        self.__txt_window = TextEdit(self, 100, 20, 800, 520, "white", 5, self._application.account.app_config.regular_font, 16)
        with open("resources/help.txt", "r") as f:
            self.__txt_window.insertPlainText(f.read())

        self._widgets += [self.__back, self.__txt_window]
        
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class LeaderboardScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self, application, max_size):

        super().__init__(application, max_size)

        self.__title = Label(self, "LEADERBOARD", 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__table = TableWidget(self, 50, 125, 600, 450, self._application.account.app_config.regular_font, 18, self._application.account.app_config.colour2_translucent, 25, 3)
        self.__show_default_leaderboard()

        gamemode_options = []
        for mode in ("Normal", "Killer"):
            for board_size in (milestone_options := ["4x4", "6x6", "9x9", "12x12", "16x16"]):
                for difficulty in ("Easy", "Medium", "Hard", "Expert"):
                    gamemode_options.append(f"{mode} {board_size} {difficulty}")

        self.__type_label = Label(self, "Leaderboard Options", 700, 125, 250, 40, self._application.account.app_config.regular_font, 18)
        
        self.__type = ComboBox(self, 700, 175, 250, 40, self._application.account.app_config.regular_font, 18, ["Best Time", "Milestone"])
        self.__type.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__type.activated.connect(self.__show_options)

        self.__next_label = Label(self, "", 700, 225, 250, 40, self._application.account.app_config.regular_font, 18)

        self.__gamemode = ComboBox(self, 700, 275, 250, 40, self._application.account.app_config.regular_font, 18, gamemode_options)
        self.__gamemode.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__gamemode.activated.connect(partial(self.__update_table, "gamemode"))
        self.__gamemode.hide()

        self.__milestone = ComboBox(self, 700, 275, 250, 40, self._application.account.app_config.regular_font, 18, milestone_options)
        self.__milestone.setStyleSheet(f"background: {self._application.account.app_config.colour2}; border: 2px solid black;")
        self.__milestone.activated.connect(partial(self.__update_table, "milestone"))
        self.__milestone.hide()

        self._widgets += [self.__back, self.__title, self.__table, self.__type, self.__gamemode, 
                          self.__milestone, self.__type_label, self.__next_label]  
    
    def __show_options(self):
        if self.__type.currentText() == "Best Time":
            self.__gamemode.show()
            self.__milestone.hide()
            self.__next_label.setText("Choose Gamemode")
        elif self.__type.currentText() == "Milestone":
            self.__gamemode.hide()
            self.__milestone.show()
            self.__next_label.setText("Choose Milestone")
        else:
            self.__gamemode.hide()
            self.__milestone.hide()
            self.__next_label.setText("")
            self.__show_default_leaderboard()
    
    def __show_default_leaderboard(self):
        headings = ["Player Username", "Rating", "Title"]
        self.__table.load_data(headings, database.all_account_rating_data())
    
    def __update_table(self, mode):
        if mode == "gamemode" and (txt := self.__gamemode.currentText()):
            mode, bs, difficulty = txt.split(" ")
            board_size = int(bs.split("x")[0])
            headings = ["Player Username", "Rating", "Title", f"Best Time ({txt})"]
            self.__table.load_data(headings, database.leaderboard_best_time_data(mode, board_size, difficulty))
        elif mode == "milestone" and (board_size := self.__milestone.currentText()):
            headings = ["Player Username", "Rating", "Title", f"Milestone Completions ({board_size})"]
            self.__table.load_data(headings, database.leaderboard_milestone_data(board_size))
        else:
            self.__show_default_leaderboard()
            self.statusBar().showMessage("Please select an option to continue")
        
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GUI(UI): # Graphical User Interface (GUI) class

    def __init__(self): # Constructor

        super().__init__() # Inherit from UI

        self.__pyqt_app = QApplication(argv) # Create PyQt GUI Application
        self.__max_size = self.__pyqt_app.primaryScreen().size() # Create maximum size (for maximising the window)

        with open("options.json") as f: # Load in options file
            self.__options = json.load(f)

        # Initialise fonts used in GUI
        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        self.__screens = {} # Placeholder screens dictionary to make it easier to load and render screens
        self.__screen_partials = {"home": self.__home_screen, "open or create new game": self.__open_or_create_new_game_screen,
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
        home_screen.play_singleplayer_signal.connect(partial(self.__show_screen, "open or create new game", self.__open_or_create_new_game_screen))
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
    
    def __open_or_create_new_game_screen(self): # Initialise open or create new game screen
        open_or_create_new_game_screen = OpenOrCreateNewGameScreen(self._application, self.__max_size)
        open_or_create_new_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_or_create_new_game_screen.open_game_signal.connect(partial(self.__show_screen, "open game", self.__open_game_screen))
        open_or_create_new_game_screen.create_new_game_signal.connect(partial(self.__show_screen, "config game", self.__config_game_screen))  
        return open_or_create_new_game_screen
    
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

    def __game_screen(self): # Initialise game screen
        game_screen = GameScreen(self._application, self.__max_size)
        game_screen.return_to_home_screen_signal.connect(self.__quit_game)
        game_screen.save_stats_signal.connect(self._application.save_game_stats)
        game_screen.update_rating_signal.connect(self._application.update_singleplayer_rating)
        game_screen.update_milestone_signal.connect(self._application.update_milestone)
        return game_screen

    def __create_new_account_screen(self): # Initialise create new account screen
        create_new_account_screen = CreateNewAccountScreen(self._application, self.__max_size)
        create_new_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        create_new_account_screen.create_account_signal.connect(self.__create_new_account)
        return create_new_account_screen

    def __sign_in_screen(self): # Initialise sign in screen
        sign_in_screen = SignInScreen(self._application, self.__max_size)
        sign_in_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        sign_in_screen.sign_in_signal.connect(self.__sign_in)
        return sign_in_screen

    def __manage_account_screen(self): # Initialise manage account screen
        manage_account_screen = ManageAccountScreen(self._application, self.__max_size)
        manage_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        manage_account_screen.change_username_signal.connect(self._application.change_username)
        manage_account_screen.change_password_signal.connect(self._application.change_password)
        manage_account_screen.delete_account_signal.connect(self._application.delete_account)
        return manage_account_screen

    def __view_gui_presets_screen(self): # Initialise view gui presets screen
        view_gui_presets_screen = ViewGUIPresetsScreen(self._application, self.__max_size)
        view_gui_presets_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        view_gui_presets_screen.update_preset_signal.connect(self.__show_edit_gui_preset_screen)
        view_gui_presets_screen.use_preset_signal.connect(self._application.use_gui_preset)
        return view_gui_presets_screen
    
    def __edit_gui_preset_screen(self, mode, preset_id): # Initialise edit gui preset screen
        edit_gui_preset_screen = EditGUIPresetScreen(self._application, self.__max_size, mode, preset_id)
        edit_gui_preset_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        edit_gui_preset_screen.save_signal.connect(self._application.update_appearance_preset)
        edit_gui_preset_screen.delete_signal.connect(self._application.delete_appearance_preset)
        return edit_gui_preset_screen
    
    def __view_stats_screen(self): # Initialise view stats screen
        view_stats_screen = ViewStatsScreen(self._application, self.__max_size)
        view_stats_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return view_stats_screen
    
    def __game_milestones_screen(self): # Initialise game milestones screen
        game_milestones_screen = GameMilestonesScreen(self._application, self.__max_size)
        game_milestones_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        game_milestones_screen.claim_reward_signal.connect(self._application.claim_reward)
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
        bonus_hints = 0 if self._application.account.username is None else database.bonus_hints(self._application.account.username)
        self.__game.generate(mode, difficulty, board_size, timed, hardcore, bonus_hints)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __load_game_screen(self, file): # Load game screen (load from file)
        self.__game = Game()
        self.__game.load_game(self._application.account.username, file)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __show_edit_gui_preset_screen(self, options):
        mode, preset_id = options
        self.__screens["edit gui preset"] = self.__edit_gui_preset_screen(mode, preset_id)
        self.__push_screen("edit gui preset")
        
    def __quit_game(self): # Quit game screen (returns to home screen)
        self.__close_curr_screen()
        for _ in range(3):
            self._pop_ui_from_stack()
        self.__show_screen(self._get_curr_ui(), self.__screen_partials[self._get_curr_ui()])
    
    def __create_new_account(self, options):
        try:
            self._application.create_account(options)
            self.__pop_screen()
        except DBError as err:
            self.__screens["create new account"].show_error(err)

    def __sign_in(self, options):
        try:
            self._application.sign_in(options)
            self.__pop_screen()
        except DBError as err:
            self.__screens["sign in"].show_error(err)

    def __sign_out(self): # Method to sign out
        self._application.sign_out()
        self.__close_curr_screen()
        self.__show_screen("home", self.__screen_partials["home"])
        
    def run(self): # run function executed by sudoku.py
        exit(self.__pyqt_app.exec())
