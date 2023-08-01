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
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QGridLayout

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

class BackButton(Button):
    def __init__(self, window, command):
        super().__init__(window, "", 925, 15, 60, 60, QFont("Metropolis", 20), command)
        self.setIcon(QIcon("resources/back.svg"))
        self.setIconSize(QSize(60, 60))
        self.setStyleSheet("border-radius:30px;")
        
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

        play_singleplayer_button = Button(self, "PLAY SINGLEPLAYER", 300, 250, 400, 50, QFont("Metropolis", 25), self.play_singleplayer)
        play_multiplayer_button = Button(self, "PLAY MULTIPLAYER", 300, 320, 400, 50, QFont("Metropolis", 25), None)
        leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, QFont("Metropolis", 25), None)

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
    play_game_signal = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        title = Label(self, "CREATE NEW GAME", 0, 25, 1000, 100, QFont("LIBRARY 3 AM soft", 50))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        play = Button(self, "PLAY GAME", 675, 290, 200, 50, QFont("Metropolis", 20), self.play_game)
        back = BackButton(self, self.return_to_home_screen)

        mode = Label(self, "MODE: ", 50, 225, 300, 100, QFont("Metropolis", 24))
        difficulty = Label(self, "DIFFICULTY: ", 50, 150, 300, 100, QFont("Metropolis", 24))
        timed = Label(self, "TIMED: ", 50, 300, 300, 100, QFont("Metropolis", 24))
        time_control = Label(self, "TIME CONTROL: ", 50, 375, 300, 100, QFont("Metropolis", 24))

        mode_menu = ComboBox(self, 330, 175, 200, 50, QFont("Metropolis", 20), ["Normal"])
        difficulty_menu = ComboBox(self, 330, 250, 200, 50, QFont("Metropolis", 20), ["Easy", "Medium", "Hard", "Challenge"])
        timed_menu = ComboBox(self, 330, 325, 200, 50, QFont("Metropolis", 20), ["Yes", "No"])
        time_control_menu = ComboBox(self, 330, 400, 200, 50, QFont("Metropolis", 20), ["5 mins", "10 mins", "15 mins", "30 mins", "1 hour"])

    def play_game(self):
        self.play_game_signal.emit()

    def return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(QMainWindow):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        title = Label(self, "S U D O K U", 0, 10, 1000, 100, QFont("LIBRARY 3 AM soft", 40))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        back = BackButton(self, self.return_to_home_screen)

        PADDING, STARTY = 20, 90
        GRIDSIZE = (560 - STARTY - PADDING) // 9
        STARTX = (1000 - 9 * GRIDSIZE) // 2

        for row in range(9):
            for col in range(9):
                square = Button(self, "0", STARTX + GRIDSIZE*col, STARTY + GRIDSIZE*row, GRIDSIZE, GRIDSIZE, QFont("Metropolis", 20), None)
    
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

        self.__home_screen = HomeScreen()
        self.__home_screen.play_singleplayer_signal.connect(self.__show_config_game_screen)
        self.__home_screen.create_new_account_signal.connect(self.__show_create_new_account_screen)

        self.__config_game_screen = ConfigGameScreen()
        self.__config_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        self.__config_game_screen.play_game_signal.connect(self.__show_game_screen)

        self.__game_screen = GameScreen()
        self.__game_screen.return_to_home_screen_signal.connect(self.__quit_game)

        self.__create_new_account_screen = CreateNewAccountScreen()

        self.__screens = {"home": self.__home_screen, "config game": self.__config_game_screen, 
                          "game": self.__game_screen, "create new account": self.__create_new_account_screen}

        self._push_ui_to_stack("home")
        self.__home_screen.show()

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
        self.__push_screen("config game")
    
    def __show_game_screen(self):
        self.__push_screen("game")
    
    def __show_create_new_account_screen(self):
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
