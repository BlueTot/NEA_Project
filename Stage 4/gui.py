from sys import argv, exit
import os
from functools import partial
from board import GameError
from game import Game
from ui import UI

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget, QTextEdit

class Button(QPushButton): # Screen Button
    def __init__(self, window, text, x, y, width, height, font, command):
        super().__init__(text, window)
        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font))
        if command is not None:
            self.clicked.connect(command)

class Border(QPushButton): # Border for number grid
    def __init__(self, window, x, y, width, height, border_width):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setStyleSheet("QPushButton{" + f"border: {border_width}px solid black;" + "}")

class Action(QAction): # Action for toolbar
    def __init__(self, window, image, text, command, checkable):
        if image is None:
            super().__init__(text, window)
        else:
            super().__init__(image, text, window)
        self.setCheckable(checkable)
        if command is not None:
            self.triggered.connect(command)

class MenuButton(QPushButton): # Menu in a button for toolbar
    def __init__(self, window, icon, size, font, actions):
        super().__init__(window)
        self.setIcon(icon)
        self.setIconSize(size) 
        menu = QMenu()
        menu.setFont(font)
        for action, command in actions:
            menu.addAction(Action(self, None, action, command, False))
        self.setMenu(menu)

        self.setStyleSheet("QPushButton::menu-indicator {width:0px;}")

class Label(QLabel): # Screen label
    def __init__(self, window, text, x, y, width, height, font):
        super().__init__(window)
        self.setText(text)
        self.setGeometry(x, y, width, height)
        self.setFont(font)

class ComboBox(QComboBox): # Screen ComboBox to input data
    def __init__(self, window, x, y, width, height, font, options):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setFont(font)
        self.addItem("")
        self.addItems(options)

class ProgressBar(QProgressBar): # Progress bar to display game progress
    def __init__(self, window, x, y, width, height):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setTextVisible(True)
        self.setValue(0)

class CircularButton(Button): # Screen button that is circular and has a border
    def __init__(self, window, x, y, width, height, image, command):
        super().__init__(window, "", x, y, width, height, QFont("Metropolis", 20), command)
        self.setIcon(image)
        self.setIconSize(QSize(width, height))
        self.setStyleSheet("border-radius:" + str(width//2) + "px;")
    
class BackButton(CircularButton): # Back button to return to previous page
    def __init__(self, window, command):
        super().__init__(window, 925, 15, 60, 60, QIcon("resources/back.svg"), command)

class Screen(QMainWindow): # Screen
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))
        self.statusBar().setFont(QFont("Metropolis", 14))
        self.statusBar().setStyleSheet("QStatusBar{color:red;}")
        
class HomeScreen(Screen):

    play_singleplayer_signal = pyqtSignal()
    create_new_account_signal = pyqtSignal()
    help_signal = pyqtSignal()

    def __init__(self):

        super().__init__()
        
        self.__title = Label(self, "S U D O K U", 0, 75, 1000, 100, QFont("LIBRARY 3 AM soft", 70))
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play_singleplayer_button = Button(self, "PLAY SINGLEPLAYER", 300, 250, 400, 50, QFont("Metropolis", 25), self.__play_singleplayer)
        self.__play_multiplayer_button = Button(self, "PLAY MULTIPLAYER", 300, 320, 400, 50, QFont("Metropolis", 25), None)
        self.__leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, QFont("Metropolis", 25), None)

        toolbar = QToolBar(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar)
        toolbar.setIconSize(QSize(60, 60))
        toolbar.setStyleSheet("background : rgb(150, 150, 150)")
        toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.__quit_game, False))
        toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Create Account", self.__create_new_account), ("Sign In", None), ("Sign Out", None), ("Show Stats", None),]))
        toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Customise GUI", None), ("Manage Account", None)]))
        toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", self.__help_screen, False))

    def __play_singleplayer(self):
        self.play_singleplayer_signal.emit()
    
    def __create_new_account(self):
        self.create_new_account_signal.emit()
    
    def __help_screen(self):
        self.help_signal.emit()

    def __quit_game(self):
        exit()

class OpenOrCreateNewGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    create_new_game_signal = pyqtSignal()
    open_game_signal = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.__open_game_button = Button(self, "OPEN EXISTING GAME", 70, 80, 400, 400, QFont("Metropolis", 25), self.__open_game)
        self.__open_game_button.setStyleSheet("background: #ffcccb; border: 5px solid black;")
        self.__create_new_game_button = Button(self, "CREATE NEW GAME", 530, 80, 400, 400, QFont("Metropolis", 25), self.__create_new_game)
        self.__create_new_game_button.setStyleSheet("background: #aee8f5; border: 5px solid black;")

        self.__back_button = BackButton(self, self.__return_to_home_screen)
    
    def __open_game(self):
        if os.listdir("games"):
            self.open_game_signal.emit()
        else:
            self.statusBar().showMessage("*There are no saved games at this moment, please create a new game")

    def __create_new_game(self):
        self.create_new_game_signal.emit()

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class OpenGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    play_game_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.__title = Label(self, "OPEN EXISTING GAME", 0, 25, 1000, 100, QFont("LIBRARY 3 AM soft", 50))
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, QFont("Metropolis", 20), self.__play_game)
        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__choose_game = Label(self, "CHOOSE A GAME: ", 50, 150, 300, 100, QFont("Metropolis", 20))
        self.__choose_game_menu = ComboBox(self, 50, 230, 400, 50, QFont("Metropolis", 15), os.listdir(Game.DEFAULT_DIRECTORY))
        self.__choose_game_menu.activated.connect(self.__show_game_info)

        self.statusBar().setFont(QFont("Metropolis", 14))
        self.statusBar().setStyleSheet("QStatusBar{color:red;}")

        self.__game_info = QTextEdit(self)
        self.__game_info.setGeometry(50, 300, 400, 235)
        self.__game_info.setStyleSheet("background: #aee8f5; border: 2px solid black;")
        self.__game_info.setFont(QFont("Metropolis", 18))
        self.__game_info.setReadOnly(True)
    
    def __show_game_info(self):
        if file := self.__choose_game_menu.currentText():
            stats = Game.get_stats_from(file)
            labels = ["Creation Date", "Creation Time", "Mode", "Difficulty"]
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
    play_game_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.__title = Label(self, "CREATE NEW GAME", 0, 25, 1000, 100, QFont("LIBRARY 3 AM soft", 50))
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, QFont("Metropolis", 20), self.__play_game)
        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__mode = Label(self, "MODE: ", 50, 150, 300, 100, QFont("Metropolis", 24))
        self.__difficulty = Label(self, "DIFFICULTY: ", 50, 225, 300, 100, QFont("Metropolis", 24))
        self.__timed = Label(self, "TIMED: ", 50, 300, 300, 100, QFont("Metropolis", 24))
        self.__time_control = Label(self, "TIME CONTROL: ", 50, 375, 300, 100, QFont("Metropolis", 24))

        self.__mode_menu = ComboBox(self, 330, 175, 200, 50, QFont("Metropolis", 20), ["Normal"])
        self.__difficulty_menu = ComboBox(self, 330, 250, 200, 50, QFont("Metropolis", 20), ["Easy", "Medium", "Hard", "Challenge"])
        self.__timed_menu = ComboBox(self, 330, 325, 200, 50, QFont("Metropolis", 20), ["Yes", "No"])
        self.__time_control_menu = ComboBox(self, 330, 400, 200, 50, QFont("Metropolis", 20), ["5 mins", "10 mins", "15 mins", "30 mins", "1 hour"])

    def __play_game(self):
        if difficulty := self.__difficulty_menu.currentText():
            self.play_game_signal.emit(difficulty)
        else:
            self.statusBar().showMessage("*To continue, please fill all boxes")

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    PADDING, STARTX = 25, 10
    GRIDSIZE = (560 - 2 * PADDING) // 9

    def __init__(self):
        
        super().__init__()

        self.__selected_square = (None, None)
        self.__notes_mode = False
        self.__running = True

        self.__timer = Button(self, "00:00", 610, 20, 130, 65, QFont("Metropolis", 26), self.__pause_game)
        self.__timer.setStyleSheet("border: 2px solid black;")
        self.__progress = ProgressBar(self, 610, 110, 330, 20)
        self.__progress.setStyleSheet("QProgressBar::chunk{background-color: #99d9ea;}")

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.__info_label = Label(self, "", 595, 15, 310, 90, QFont("Metropolis", 15))
        self.__info_label.setStyleSheet("background: #aee8f5; border: 2px solid black; border-radius: 30px;")
        self.__info_label.hide()
        self.__info_button = CircularButton(self, 845, 15, 60, 60, QIcon("resources/info.svg"), self.__toggle_info_screen)

        NUM_INP_SIZE = 110
        STARTX, STARTY = 610, 130
        for ridx in range(3):
            for cidx in range(3):
                num_input = Button(self, str(num := ridx*3+cidx+1), STARTX+NUM_INP_SIZE*cidx, STARTY+NUM_INP_SIZE*ridx, NUM_INP_SIZE, NUM_INP_SIZE, QFont("Metropolis", 20), partial(self.__place_num, num))

        self.__undo_button = CircularButton(self, 610, 470, 58, 58, QIcon("resources/undo.svg"), self.__undo_move)
        self.__delete_button = CircularButton(self, 677, 470, 58, 58, QIcon("resources/delete.svg"), self.__remove_num)
        self.__delete_button.setIconSize(QSize(53, 53))
        self.__delete_button.setStyleSheet("QPushButton{border-radius: 29px; border: 5px solid black;}")
        self.__hint_button = CircularButton(self, 744, 470, 58, 58, QIcon("resources/hint.svg"), self.__show_hint)
        self.__notes_button = CircularButton(self, 811, 470, 58, 58, QIcon("resources/notes_off.svg"), self.__toggle_notes_mode)
        self.__notes_button.setIconSize(QSize(53, 53))
        self.__notes_button.setStyleSheet("QPushButton{border-radius: 29px; border: 5px solid black;}")
        self.__resign_button = CircularButton(self, 878, 470, 58, 58, QIcon("resources/resign.svg"), partial(self.__show_end_screen, False))

        self.__show_border()

    def __show_border(self):

        big_border = Border(self, self.STARTX+self.PADDING-3, self.PADDING-3, 
                            self.GRIDSIZE*9+6+6, self.GRIDSIZE*9+6+6, 3)
        big_border.show()
        for row in range(3):
            for col in range(3):
                border = Border(self, self.STARTX + self.PADDING + self.GRIDSIZE*3*col + 3*col, 
                                self.PADDING + self.GRIDSIZE*3*row + 3*row, 
                                self.GRIDSIZE*3+3, self.GRIDSIZE*3+3, 3)
                border.show()

    def set_game(self, game : Game):

        self.__game = game
        self.__info_label.setText(f"Mode: {self.__game.mode} \nDifficulty: {self.__game.difficulty} \nTime Control: ---")
        self.__create_curr_grid()
        self.__progress.setValue(int(self.__game.percent_complete()))

        self.__board_cover = QWidget(self)
        self.__board_cover.setGeometry(self.STARTX+self.PADDING-3, self.PADDING-3, width:= self.GRIDSIZE*9+12, height := self.GRIDSIZE*9+12)
        self.__board_cover.setStyleSheet("background: #aee8f5; border: 5px solid black;")
        self.__paused_label = Label(self.__board_cover, "GAME PAUSED", 0, 0, width, height, QFont("Metropolis", 24))
        self.__paused_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__board_cover.hide()

    def __create_number_grid(self, curr_board, orig_board):
        self.__sqrs = [[0 for _ in range(9)] for _ in range(9)]
    
        for row, row_lst in enumerate(curr_board):
            for col, sq in enumerate(row_lst):
                square = Button(window = self, 
                                text = str(sq.num) if sq.num != 0 else self.__game.note_at(row, col),
                                x = self.STARTX + self.PADDING + self.GRIDSIZE*col + 3*(col//3),
                                y = self.PADDING + self.GRIDSIZE*row + 3*(row//3), 
                                width = self.GRIDSIZE, 
                                height = self.GRIDSIZE, 
                                font = QFont("Metropolis", 20 if sq.num != 0 else 13), 
                                command = partial(self.__select_square, row+1, col+1))
                square.setFont(QFont("Metropolis", 20 if sq.num != 0 else 13))
                square.setStyleSheet("QPushButton{border: 2px solid black; background-color:" + 
                                     ("#99d9ea" if (row+1, col+1) == self.__selected_square else "white") + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if sq.num != 0 else "red")) + 
                                     (";text-align: left" if sq.num == 0 else "") + 
                                     ";}")
                
                self.__sqrs[row][col] = square
                square.show()

    def __update_number_grid(self, curr_board, orig_board):
        for row, row_lst in enumerate(self.__sqrs):
            for col, sq in enumerate(row_lst):
                sq.setText(str(num) if (num := curr_board[row][col].num) != 0 else self.__game.note_at(row, col))
                sq.setFont(QFont("Metropolis", 20 if num != 0 else 13))
                sq.setStyleSheet("QPushButton{border: 2px solid black; background-color:" + 
                                     ("#99d9ea" if (row+1, col+1) == self.__selected_square else "white") + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if num != 0 else "red")) + 
                                     (";text-align: left" if num == 0 else "") + 
                                     ";}")
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
        self.__game.remove_game_file()

        bg = QWidget(self)
        bg.setGeometry(0, 0, 1000, 560)
        bg.setStyleSheet("QWidget{background: rgba(153, 217, 234, 150);}")
        bg.show()

        window = QWidget(self)
        window.setGeometry(200, 30, 600, 500)
        window.setStyleSheet("QWidget{background:white; border: 5px solid black;}")
        window.show()
    
        title = Label(self, "You Won!" if win else "Game Over!", 0, 50, 1000, 100, QFont("LIBRARY 3 AM soft", 40))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.show()

        rating = Label(self, "500", 0, 200, 1000, 100, QFont("Metropolis", 60))
        rating.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        rating.show()

        home_screen_button = Button(self, "RETURN TO HOME", 350, 450, 300, 50, QFont("Metropolis", 20), self.__return_to_home_screen)
        home_screen_button.show()

        solution_button = Button(self, "SEE SOLUTION", 350, 390, 300, 50, QFont("Metropolis", 20),self.__show_solution_screen)
        if not win:
            solution_button.show()
    
    def __show_solution_screen(self):

        bg = QWidget(self)
        bg.setGeometry(0, 0, 1000, 560)
        bg.setStyleSheet("QWidget{background: white;}")
        bg.show()
        
        self.__show_border()
        self.__create_solution_grid()

        home_screen_button = Button(self, "RETURN TO HOME", 625, 250, 300, 50, QFont("Metropolis", 20), self.__return_to_home_screen)
        home_screen_button.show()

    def __show_error(self, err):
        self.statusBar().showMessage(str(err.args[0]))
    
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
                    self.__game.put_down_number(self.__selected_square[0], self.__selected_square[1], num)            
            except GameError as err:
                self.__show_error(err)
            self.__selected_square = (None, None)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
        if self.__game.is_complete():
            self.__show_end_screen(True)
            
    def __remove_num(self):
        if self.__running:
            try:
                self.__game.remove_number(self.__selected_square[0], self.__selected_square[1])
            except GameError as err:
                self.__show_error(err)
            self.__selected_square = (None, None)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
    
    def __show_hint(self):
        if self.__running:
            try:
                hint_lst = self.__game.get_hint_at(self.__selected_square[0], self.__selected_square[1])
                self.__game.add_hint_to_notes(self.__selected_square[0], self.__selected_square[1], hint_lst)
            except GameError as err:
                self.__show_error(err)
            self.__selected_square = (None, None)
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
        self.__timer.setStyleSheet(f"background: {'white' if self.__running else '#aee8f5'}; border: 2px solid black;")
        self.__board_cover.setHidden(not self.__board_cover.isHidden())

    def __return_to_home_screen(self):
        if self.__running: # game quit from the "back" button
            self.__game.save_game()
        self.return_to_home_screen_signal.emit()

class CreateNewAccountScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    
    def __init__(self):

        super().__init__()

        self.__back = BackButton(self, self.__return_to_home_screen)
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class HelpScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.back = BackButton(self, self.__return_to_home_screen)
        self.setStyleSheet("background: rgb(150, 150, 150);")

        self.txt_window = QTextEdit(self)
        self.txt_window.setGeometry(100, 20, 800, 520)
        self.txt_window.setStyleSheet("QTextEdit{background: white; border: 5px solid black;}")
        self.txt_window.setFont(QFont("Metropolis", 20))
        self.txt_window.setReadOnly(True)
        self.txt_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        with open("resources/help.txt", "r") as f:
            self.txt_window.insertPlainText(f.read())
        
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GUI(UI):

    def __init__(self):

        super().__init__()

        self.__app = QApplication(argv)

        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        self.__screens = {"home": self.__home_screen(), "open or create new game": self.__open_or_create_new_game_screen(),
                           "config game": self.__config_game_screen(), "open game": self.__open_game_screen(),
                           "game": self.__game_screen(), "create new account": self.__create_new_account_screen(), 
                           "help": self.__help_screen()}

        self.__screens["home"].show()
    
    def __home_screen(self):
        home_screen = HomeScreen()
        home_screen.play_singleplayer_signal.connect(self.__show_open_or_create_new_game_screen)
        home_screen.create_new_account_signal.connect(self.__show_create_new_account_screen)
        home_screen.help_signal.connect(self.__show_help_screen)
        return home_screen
    
    def __open_or_create_new_game_screen(self):
        open_or_create_new_game_screen = OpenOrCreateNewGameScreen()
        open_or_create_new_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_or_create_new_game_screen.open_game_signal.connect(self.__show_open_game_screen)
        open_or_create_new_game_screen.create_new_game_signal.connect(self.__show_config_game_screen)  
        return open_or_create_new_game_screen
    
    def __open_game_screen(self):
        open_game_screen = OpenGameScreen()
        open_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_game_screen.play_game_signal.connect(self.__load_game_screen)
        return open_game_screen

    def __config_game_screen(self):
        config_game_screen = ConfigGameScreen()
        config_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        config_game_screen.play_game_signal.connect(self.__show_game_screen)
        return config_game_screen

    def __game_screen(self):
        game_screen = GameScreen()
        game_screen.return_to_home_screen_signal.connect(self.__quit_game)
        return game_screen

    def __create_new_account_screen(self):
        create_new_account_screen = CreateNewAccountScreen()
        create_new_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return create_new_account_screen

    def __help_screen(self):
        help_screen = HelpScreen()
        help_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return help_screen

    def __close_curr_screen(self):
        self.__screens[self._get_curr_ui()].close()
    
    def __show_curr_screen(self):
        self.__screens[self._get_curr_ui()].show()
   
    def __push_screen(self, screen):
        self.__close_curr_screen()
        self._push_ui_to_stack(screen)
        self.__show_curr_screen()
        
    def __pop_screen(self):
        self.__close_curr_screen()
        self._pop_ui_from_stack()
        self.__show_curr_screen()
    
    def __show_open_or_create_new_game_screen(self):
        self.__screens["open or create new game"] = self.__open_or_create_new_game_screen()
        self.__push_screen("open or create new game")
    
    def __show_open_game_screen(self):
        self.__screens["open game"] = self.__open_game_screen()
        self.__push_screen("open game")
    
    def __show_config_game_screen(self):
        self.__screens["config game"] = self.__config_game_screen()
        self.__push_screen("config game")
    
    def __show_game_screen(self, difficulty):
        self.__game = Game(difficulty)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __load_game_screen(self, file):
        self.__game = Game()
        self.__game.load_game(file)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __show_create_new_account_screen(self):
        self.__screens["create new account"] = self.__create_new_account_screen()
        self.__push_screen("create new account")
    
    def __show_help_screen(self):
        self.__screens["help"] = self.__help_screen()
        self.__push_screen("help")
    
    def __quit_game(self):
        self.__close_curr_screen()
        for _ in range(3):
            self._pop_ui_from_stack()
        self.__show_curr_screen()

    def run(self):
        exit(self.__app.exec())
