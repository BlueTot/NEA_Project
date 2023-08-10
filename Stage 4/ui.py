from sys import argv, exit
import typing

from PyQt6 import QtCore
from stack import Stack
from os import system
from functools import partial
from abc import ABC, abstractmethod
from colorama import Fore, Style
from board import BoardError
from game import Game

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget, QTextEdit

class UI(ABC):

    VERSION = "v0.4"

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
        self.addItem("")
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
    help_signal = pyqtSignal()

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
        toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Create Account", self.create_new_account), ("Sign In", None), ("Sign Out", None), ("Show Stats", None),]))
        toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), QSize(60, 60), QFont("Metropolis", 15), [("Customise GUI", None), ("Manage Account", None)]))
        toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", self.help_screen, False))

    def play_singleplayer(self):
        self.play_singleplayer_signal.emit()
    
    def create_new_account(self):
        self.create_new_account_signal.emit()
    
    def help_screen(self):
        self.help_signal.emit()

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

        self.mode_menu = ComboBox(self, 330, 175, 200, 50, QFont("Metropolis", 20), ["Normal"])
        self.difficulty_menu = ComboBox(self, 330, 250, 200, 50, QFont("Metropolis", 20), ["Easy", "Medium", "Hard", "Challenge"])
        self.timed_menu = ComboBox(self, 330, 325, 200, 50, QFont("Metropolis", 20), ["Yes", "No"])
        self.time_control_menu = ComboBox(self, 330, 400, 200, 50, QFont("Metropolis", 20), ["5 mins", "10 mins", "15 mins", "30 mins", "1 hour"])

    def play_game(self):
        if difficulty := self.difficulty_menu.currentText():
            self.play_game_signal.emit(difficulty)
        else:
            self.statusBar().showMessage("*To continue, please fill all boxes")

    def return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(QMainWindow):

    return_to_home_screen_signal = pyqtSignal()

    PADDING, STARTX = 25, 10
    GRIDSIZE = (560 - 2 * PADDING) // 9

    def __init__(self):
        
        super().__init__()

        self.__selected_square = (None, None)
        self.__notes_mode = False
        self.__running = True

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))
        
        self.statusBar().setStyleSheet("QStatusBar{color:red;}")
        self.statusBar().setFont(QFont("Metropolis", 14))

        self.__timer = Button(self, "00:00", 610, 20, 130, 65, QFont("Metropolis", 26), None)
        self.__progress = ProgressBar(self, 610, 110, 330, 20)
        self.__progress.setStyleSheet("QProgressBar::chunk{background-color: #99d9ea;}")

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.__info_label = Label(self, "", 620, 15, 285, 100, QFont("Metropolis", 15))
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

    def __create_number_grid(self, curr_board, orig_board):
        self.__sqrs = [[0 for _ in range(9)] for _ in range(9)]
    
        for row, row_lst in enumerate(curr_board):
            for col, num in enumerate(row_lst):
                square = Button(window = self, 
                                text = str(num) if num != 0 else self.__game.note_at(row, col),
                                x = self.STARTX + self.PADDING + self.GRIDSIZE*col + 3*(col//3),
                                y = self.PADDING + self.GRIDSIZE*row + 3*(row//3), 
                                width = self.GRIDSIZE, 
                                height = self.GRIDSIZE, 
                                font = QFont("Metropolis", 20 if num != 0 else 13), 
                                command = partial(self.__select_square, row+1, col+1))
                square.setFont(QFont("Metropolis", 20 if num != 0 else 13))
                square.setStyleSheet("QPushButton{border: 2px solid black; background-color:" + 
                                     ("#99d9ea" if (row+1, col+1) == self.__selected_square else "white") + 
                                     ";color:" + ("black" if orig_board[row][col] != 0 else ("blue" if num != 0 else "red")) + 
                                     (";text-align: left" if num == 0 else "") + 
                                     ";}")
                
                self.__sqrs[row][col] = square
                square.show()

    def __update_number_grid(self, curr_board, orig_board):
        for row, row_lst in enumerate(self.__sqrs):
            for col, sq in enumerate(row_lst):
                sq.setText(str(num) if (num := curr_board[row][col]) != 0 else self.__game.note_at(row, col))
                sq.setFont(QFont("Metropolis", 20 if num != 0 else 13))
                sq.setStyleSheet("QPushButton{border: 2px solid black; background-color:" + 
                                     ("#99d9ea" if (row+1, col+1) == self.__selected_square else "white") + 
                                     ";color:" + ("black" if orig_board[row][col] != 0 else ("blue" if num != 0 else "red")) + 
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

    def __select_square(self, row, col):
        if self.__running:
            self.__selected_square = (row, col)
            self.__update_curr_grid()

    def __place_num(self, num):
        try:
            if self.__notes_mode:
                self.__game.edit_note(self.__selected_square[0], self.__selected_square[1], num)
            else:
                self.__game.put_down_number(self.__selected_square[0], self.__selected_square[1], num)            
        except BoardError as err:
            self.__show_error(err)
        self.__selected_square = (None, None)
        self.__update_curr_grid()
        if self.__game.is_complete():
            self.__show_end_screen(True)
            
    def __remove_num(self):
        try:
            self.__game.remove_number(self.__selected_square[0], self.__selected_square[1])
        except BoardError as err:
            self.__show_error(err)
        self.__selected_square = (None, None)
        self.__update_curr_grid()
    
    def __show_hint(self):
        try:
            hint_lst = self.__game.get_hint_at(self.__selected_square[0], self.__selected_square[1])
            self.__game.add_hint_to_notes(self.__selected_square[0], self.__selected_square[1], hint_lst)
        except BoardError as err:
            self.__show_error(err)
        self.__selected_square = (None, None)
        self.__update_curr_grid()
    
    def __toggle_notes_mode(self):
        self.__notes_mode = not self.__notes_mode
        self.__notes_button.setIcon(QIcon("resources/notes_on.svg" if self.__notes_mode else "resources/notes_off.svg"))
    
    def __undo_move(self):
        self.__game.pop_state()
        self.__game.load_state(self.__game.curr_state())
        self.__update_curr_grid()
    
    def __toggle_info_screen(self):
        self.__info_label.setHidden(not self.__info_label.isHidden())

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class CreateNewAccountScreen(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

class HelpScreen(QMainWindow):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))

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

        self.__screens = {"home": self.__home_screen(), "config game": self.__config_game_screen(), 
                          "game": self.__game_screen(), "create new account": self.__create_new_account_screen(),
                          "help": self.__help_screen()}

        self.__screens["home"].show()
    
    def __home_screen(self):
        home_screen = HomeScreen()
        home_screen.play_singleplayer_signal.connect(self.__show_config_game_screen)
        home_screen.create_new_account_signal.connect(self.__show_create_new_account_screen)
        home_screen.help_signal.connect(self.__show_help_screen)
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
    
    def __show_help_screen(self):
        self.__screens["help"] = self.__help_screen()
        self.__push_screen("help")
    
    def __quit_game(self):
        self.__close_curr_screen()
        for _ in range(2):
            self._pop_ui_from_stack()
        self.__show_curr_screen()

    def run(self):
        exit(self.__app.exec())

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
    
    def ____remove_number(self):
        try:
            while True:
                row = input("Enter the ROW you want to remove the number at: ")
                col = input("Enter the COLUMN you want to remove the number at: ")
                self.__game.__remove_number(row, col)
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
                    self.____remove_number()
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
        self.__print_board(self.__game.curr_board, self.__game.orig_board)
    
    def __print_solution(self):
        self.__print_board(self.__game.solved_board, self.__game.orig_board)
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
