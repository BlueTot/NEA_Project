from sys import argv, exit
from stack import Stack
from os import system
from abc import ABC, abstractmethod
from colorama import Fore, Style
from board import BoardError
from game import Game

from PyQt6.QtCore import QSize, Qt, QRect, QPoint
from PyQt6.QtGui import QFont, QAction, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenuBar, QMenu, QToolButton

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
    def __init__(self, text, window, x, y, width, height, font, command):
        super().__init__(text, window)
        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font))
        if command is not None:
            self.clicked.connect(command)

class Action(QAction):
    def __init__(self, window, image, text, command):
        if image is None:
            super().__init__(text, window)
        else:
            super().__init__(image, text, window)
        self.setStatusTip(text)
        if command is not None:
            self.triggered.connect(command)

class MenuButton(QPushButton):
    def __init__(self, window, icon, size, font, actions):
        super().__init__(window)
        self.setIcon(icon)
        self.setIconSize(size) 
        menu = QMenu()
        menu.setFont(font)
        for action in actions:
            menu.addAction(action)
        menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMenu(menu)
        self.setStyleSheet("QPushButton::menu-indicator {width:0px;}")

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        title = QLabel(self)
        title.setText("S U D O K U")
        title.setGeometry(0, 75, 1000, 100)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setFont(QFont("LIBRARY 3 AM soft", 70))

        play_singleplayer_button = Button("PLAY SINGLEPLAYER", self, 300, 250, 400, 50, QFont("Metropolis", 25), None)
        play_multiplayer_button = Button("PLAY MULTIPLAYER", self, 300, 320, 400, 50, QFont("Metropolis", 25), None)
        leaderboard_button = Button("LEADERBOARD", self, 300, 390, 400, 50, QFont("Metropolis", 25), None)

        toolbar = QToolBar(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar)
        toolbar.setIconSize(QSize(60, 60))
        toolbar.setStyleSheet("background : rgb(150, 150, 150)")
        toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.quit_game))
        toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), QSize(60, 60), QFont("Metropolis", 15), ["Create Account", "Sign In"]))
        toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), QSize(60, 60), QFont("Metropolis", 15), ["Customise GUI"]))
        toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", None))

    def quit_game(self):
        exit()
        
class GUI(UI):
    def __init__(self):
        super().__init__()

        self.app = QApplication(argv)
        self.window = MainWindow() 
        self.window.show()

        # self.menu = QMenu("&File", self.window)
        # #self.menu.move(100, 100)
        # self.menu.addAction(Action(self.window, QIcon("resources/exit.svg"), "Create Account", None))
        # #self.menu.popup(QPoint(100, 100))
        # self.menu.show()
    
    def run(self):
        
        self.app.exec()

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
