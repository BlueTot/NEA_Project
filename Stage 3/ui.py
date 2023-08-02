from sys import argv, exit
import typing

from PyQt6 import QtCore
from stack import Stack
from os import system
from abc import ABC, abstractmethod
from colorama import Fore, Style
from board import BoardError
from game import Game

from PyQt6.QtCore import QSize, Qt, pyqtSignal, QRect
from PyQt6.QtGui import QFont, QAction, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget

class UI(ABC):

    VERSION = "v0.3"

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

class Button(QPushButton):
    def __init__(self, window, text, x, y, width, height, font, command):
        super().__init__(text, window)
        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font))
        if command is not None:
            self.clicked.connect(command)

class Border(QPushButton):
    def __init__(self, window, x, y, width, height, border_width):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setStyleSheet("QPushButton{" + f"border: {border_width}px solid black;" + "}")

class Action(QAction):
    def __init__(self, window, image, text, command, checkable):
        if image is None:
            super().__init__(text, window)
        else:
            super().__init__(image, text, window)
        self.setCheckable(checkable)
        if command is not None:
            self.triggered.connect(command)

class MenuButton(QPushButton):
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

class Label(QLabel):
    def __init__(self, window, text, x, y, width, height, font):
        super().__init__(window)
        self.setText(text)
        self.setGeometry(x, y, width, height)
        self.setFont(font)

class ComboBox(QComboBox):
    def __init__(self, window, x, y, width, height, font, options):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setFont(font)
        self.addItems(options)

class ProgressBar(QProgressBar):
    def __init__(self, window, x, y, width, height):
        super().__init__(window)
        self.setGeometry(x, y, width, height)
        self.setTextVisible(True)
        self.setValue(0)

class CircularButton(Button):
    def __init__(self, window, x, y, width, height, image, command):
        super().__init__(window, "", x, y, width, height, QFont("Metropolis", 20), command)
        self.setIcon(image)
        self.setIconSize(QSize(width, height))
        self.setStyleSheet("border-radius:" + str(width//2) + "px;")
    
class BackButton(CircularButton):
    def __init__(self, window, command):
        super().__init__(window, 925, 15, 60, 60, QIcon("resources/back.svg"), command)
        
class HomeScreen(QMainWindow):

    play_singleplayer_signal = pyqtSignal()
    create_new_account_signal = pyqtSignal()

    def __init__(self): 

        super().__init__()
    
        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        title = Label(self, "S U D O K U", 0, 75, 1000, 100, QFont("LIBRARY 3 AM soft", 70))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.play_singleplayer_button = Button(self, "PLAY SINGLEPLAYER", 300, 250, 400, 50, QFont("Metropolis", 25), self.play_singleplayer)
        self.play_multiplayer_button = Button(self, "PLAY MULTIPLAYER", 300, 320, 400, 50, QFont("Metropolis", 25), None)
        self.leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, QFont("Metropolis", 25), None)

        toolbar = QToolBar(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar)
        toolbar.setIconSize(QSize(60, 60))
        toolbar.setStyleSheet("background : rgb(150, 150, 150)")
        toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.quit_game, False))
        toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Create Account", self.create_new_account), ("Sign In", None)]))
        toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Customise GUI", None)]))
        toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", None, False))

    def play_singleplayer(self):
        self.play_singleplayer_signal.emit()
    
    def create_new_account(self):
        self.create_new_account_signal.emit()

    def quit_game(self):
        exit()

class ConfigGameScreen(QMainWindow):

    return_to_home_screen_signal = pyqtSignal()
    play_game_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        title = Label(self, "CREATE NEW GAME", 0, 25, 1000, 100, QFont("LIBRARY 3 AM soft", 50))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.play = Button(self, "PLAY GAME", 675, 290, 200, 50, QFont("Metropolis", 20), self.play_game)
        self.back = BackButton(self, self.return_to_home_screen)

        self.statusBar().setFont(QFont("Metropolis", 14))
        self.statusBar().setStyleSheet("QStatusBar{color:red;}")

        self.mode = Label(self, "MODE: ", 50, 150, 300, 100, QFont("Metropolis", 24))
        self.difficulty = Label(self, "DIFFICULTY: ", 50, 225, 300, 100, QFont("Metropolis", 24))
        self.timed = Label(self, "TIMED: ", 50, 300, 300, 100, QFont("Metropolis", 24))
        self.time_control = Label(self, "TIME CONTROL: ", 50, 375, 300, 100, QFont("Metropolis", 24))

        self.mode_menu = ComboBox(self, 330, 175, 200, 50, QFont("Metropolis", 20), ["", "Normal"])
        self.difficulty_menu = ComboBox(self, 330, 250, 200, 50, QFont("Metropolis", 20), ["", "Easy", "Medium", "Hard", "Challenge"])
        self.timed_menu = ComboBox(self, 330, 325, 200, 50, QFont("Metropolis", 20), ["", "Yes", "No"])
        self.time_control_menu = ComboBox(self, 330, 400, 200, 50, QFont("Metropolis", 20), ["", "5 mins", "10 mins", "15 mins", "30 mins", "1 hour"])

    def play_game(self):
        if difficulty := self.difficulty_menu.currentText():
            self.play_game_signal.emit(difficulty)
        else:
            self.statusBar().showMessage("*To continue, please fill all boxes")

    def return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(QMainWindow):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        self.back = BackButton(self, self.return_to_home_screen)
    
    def set_game(self, game : Game):

        self.__game = game

        PADDING, STARTX = 20, 10
        GRIDSIZE = (560 - 2 * PADDING) // 9


        big_border = Border(self, STARTX + PADDING, PADDING, GRIDSIZE*9, GRIDSIZE*9, 5)
        for ridx in range(3):
            for cidx in range(3):
                border = Border(self, STARTX + PADDING + GRIDSIZE*3*cidx, PADDING + GRIDSIZE*3*ridx, GRIDSIZE*3, GRIDSIZE*3, 3)

        for ridx, row in enumerate(self.__game.board.get_curr_board()):
            for cidx, num in enumerate(row):
                square = Button(self, str(num) if num != 0 else "", STARTX + PADDING + GRIDSIZE*cidx, PADDING + GRIDSIZE*ridx, GRIDSIZE, GRIDSIZE, QFont("Metropolis", 20), self.clicked)
                square.setStyleSheet("QPushButton{border: 2px solid black;}")
        
        NUM_INP_SIZE = 110
        STARTX, STARTY = 610, 130
        for ridx in range(3):
            for cidx in range(3):
                num_input = Button(self, str(ridx*3+cidx+1), STARTX+NUM_INP_SIZE*cidx, STARTY+NUM_INP_SIZE*ridx, NUM_INP_SIZE, NUM_INP_SIZE, QFont("Metropolis", 20), None)
        
        timer = Button(self, "00:00", 610, 20, 130, 65, QFont("Metropolis", 26), None)
        progress = ProgressBar(self, 610, 110, 330, 20)

        undo_button = CircularButton(self, 610, 470, 60, 60, QIcon("resources/undo.svg"), None)
                

    def clicked(self):
        print("clicked")

    def return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class CreateNewAccountScreen(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

class GUI(UI):

    def __init__(self):

        super().__init__()

        self.__app = QApplication(argv)

        self.__screens = {"home": self.__home_screen(), "config game": self.__config_game_screen(), 
                          "game": self.__game_screen(), "create new account": self.__create_new_account_screen()}

        self._push_ui_to_stack("home")
        self.__screens["home"].show()
    
    def __home_screen(self):
        home_screen = HomeScreen()
        home_screen.play_singleplayer_signal.connect(self.__show_config_game_screen)
        home_screen.create_new_account_signal.connect(self.__show_create_new_account_screen)
        return home_screen

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
        return create_new_account_screen

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
    
    def __show_config_game_screen(self):
        self.__screens["config game"] = self.__config_game_screen()
        self.__push_screen("config game")
    
    def __show_game_screen(self, difficulty):
        self.__game = Game(difficulty)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __show_create_new_account_screen(self):
        self.__screens["create new account"] = self.__create_new_account_screen()
        self.__push_screen("create new account")
    
    def __quit_game(self):
        self.__close_curr_screen()
        for _ in range(2):
            self._pop_ui_from_stack()
        self.__show_curr_screen()

    def run(self):
        self.__app.exec()

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
                num = input("Enter the NUMBER you want to place: ")
                row = input("Enter the ROW you want to place the number at: ")
                col = input("Enter the COLUMN you want to place the number at: ")
                self.__game.put_down_number(row, col, num)
                break
        except BoardError as err:
            input(err)
    
    def __remove_number(self):
        try:
            while True:
                row = input("Enter the ROW you want to remove the number at: ")
                col = input("Enter the COLUMN you want to remove the number at: ")
                self.__game.remove_number(row, col)
                break
        except BoardError as err:
            input(err)
    
    def __get_hint(self):
        try:
            while True:
                row = input("Enter the ROW you want to get the hint for: ")
                col = input("Enter the COLUMN you want to get the hint for: ")
                return self.__game.get_hint_at(row, col)
        except BoardError as err:
            input(err)

    def __config_game(self):
        difficulty_num = int(self.__get_input("Press (1) for Easy, (2) for Medium, (3) for Hard, (4) for Challenge: ", [str(i) for i in range(1, 5)]))
        return Game.DIFFICULTY_NUMS[difficulty_num]

    def __play_new_game(self):
        difficulty = self.__config_game()
        self.__game = Game(difficulty)
        while True:
            self.__print_header()
            self.__print_game_stats()
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
    
    def __print_curr_board(self):
        self.__print_board(self.__game.curr_board(), self.__game.orig_board())
    
    def __print_solution(self):
        self.__print_board(self.__game.solved_board(), self.__game.orig_board())
        input("Press enter to quit game")


    def __print_header(self):
        system("cls")
        print("-"*(l := len(s := f'SUDOKU {UI.VERSION}')) + "\n" + s + "\n" + "-"*l)
    
    def __print_game_stats(self):
        print("\n" + f"MODE: {self.__game.mode}")
        print(f"BOARD SIZE: {self.__game.board_size}")
        print(f"DIFFICULTY: {self.__game.difficulty.capitalize()}")
        print(f"% COMPLETE: {self.__game.percent_complete()}%")

    def __print_hint(self, hint):
        print("HINT: The valid numbers that can be placed are ", ', '.join(list(map(str, hint))))
        input("Press enter to continue")
