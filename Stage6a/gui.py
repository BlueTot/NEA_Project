from sys import argv, exit # Import argv and edit from sys
import os # Import os module
from functools import partial # Import partial from functools module
import json # Import json module

from game import Game, GameError # Import Game class and GameError exception class
from ui import UI # Import UI
from board import to_letter # Import to_letter function
import database
from database import DBError

'''PyQt6 GUI Imports'''

from PyQt6.QtCore import QSize, Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QAction, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget, QTextEdit, QLineEdit

class AppearanceConfiguration: # Appearance Configuration class

    def __init__(self): # Constructor
        # rgb(240, 240, 240)
        self.__background_colour = "default"
        self.__colour1 = "rgb(255, 255, 255)"
        # self.__colour2 = "#C5B4E3"
        self.__colour2 = "#aee8f5"
        self.__colour2_translucent = "rgba(153, 217, 234, 150)"
        self.__colour3 = "rgb(150, 150, 150)"
        self.__colour4 = "#ffcccb"
        self.__title_font = "LIBRARY 3 AM soft"
        self.__regular_font = "Metropolis"
        self.__killer_colours = ["#FF7276", "#FFFFE0", "#ADD8E6", "#90EE90", "#C5B4E3"]
    
    '''Getters'''

    @property
    def background_colour(self): # Gets background colour
        return self.__background_colour
    
    @property
    def colour1(self): # Gets colour 1
        return self.__colour1
    
    @property
    def colour2(self): # Gets colour 2
        return self.__colour2
    
    @property
    def colour2_translucent(self): # Gets translucent version of colour 2
        return self.__colour2_translucent
    
    @property
    def colour3(self): # Gets colour 3
        return self.__colour3
    
    @property
    def colour4(self): # Gets colour 4
        return self.__colour4
    
    @property
    def title_font(self): # Gets title font family
        return self.__title_font
    
    @property
    def regular_font(self): # Gets regular font family
        return self.__regular_font
    
    @property
    def killer_colours(self): # Gets killer sudoku board colours
        return self.__killer_colours

class Button(QPushButton): # Screen Button

    def __init__(self, window, text, x, y, width, height, font_family, font_size, command): # Constructor
        super().__init__(text, window)

        # Stores original dimensions and font sizes
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        # Configures button with dimensions and font sizes
        self.setGeometry(x, y, width, height)
        if font_family is not None and font_size is not None:
            self.setFont(QFont(font_family, font_size))

        # Adds command to button
        if command is not None:
            self.clicked.connect(command)
    
    # Scale up button by scale factor
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    # Returns button to its original size
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class Border(QPushButton): # Border for number grid

    def __init__(self, window, x, y, width, height, border_width): # Constructor
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._orig_border_width = border_width

        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"border: {border_width}px solid black;")
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        self.setStyleSheet(f"border: {int(self._orig_border_width*factor)}px solid black;")
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        self.setStyleSheet(f"border: {self._orig_border_width}px solid black;")


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
        self.menu = QMenu()
        if font is not None:
            self.menu.setFont(font)
        for action, command in actions:
            self.menu.addAction(Action(self, None, action, command, False))
        self.setMenu(self.menu)
        self.setStyleSheet("QPushButton::menu-indicator {width:0px;}")

class Label(QLabel): # Screen label
    def __init__(self, window, text, x, y, width, height, font_family, font_size):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setText(text)
        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font_family, font_size))
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class ComboBox(QComboBox): # Screen ComboBox to input data
    def __init__(self, window, x, y, width, height, font_family, font_size, options):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font_family, font_size))
        self.addItem("")
        self.addItems(options)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class ProgressBar(QProgressBar): # Progress bar to display game progress
    def __init__(self, window, x, y, width, height):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height

        self.setGeometry(x, y, width, height)
        self.setTextVisible(True)
        self.setValue(0)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)

class CircularButton(Button): # Screen button that is circular and has a border
    def __init__(self, window, x, y, width, height, image, command):
        super().__init__(window, "", x, y, width, height, None, None, command)
        self.setIcon(image)
        self.setIconSize(QSize(width, height))
        self.setStyleSheet("border-radius:" + str(width//2) + "px;")
    
    def maximise(self, factor):
        super().maximise(factor)
        self.setIconSize(QSize(int(self._orig_width*factor), int(self._orig_height*factor)))
        self.setStyleSheet("border-radius:" + str(self._orig_width*factor//2) + "px;")
    
    def minimise(self):
        super().minimise()
        self.setIconSize(QSize(self._orig_width, self._orig_height))
        self.setStyleSheet("border-radius:" + str(self._orig_width//2) + "px;")
    
class BackButton(CircularButton): # Back button to return to previous page
    def __init__(self, window, command):
        super().__init__(window, 925, 15, 60, 60, QIcon("resources/back.svg"), command)

class TextEdit(QTextEdit):
    def __init__(self, window, x, y, width, height, background_colour, border_width, font_family, font_size):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"background: {background_colour}; border: {border_width}px solid black;")
        self.setFont(QFont(font_family, font_size))
        self.setReadOnly(True)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class Rect(QWidget):
    def __init__(self, window, x, y, width, height, background_colour, border_width):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._background_colour = background_colour
        self._orig_border_width = border_width
        

        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"background: {background_colour}; border: {border_width}px solid black;")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        self.setStyleSheet(f"background: {self._background_colour}; border: {int(self._orig_border_width * factor)}px solid black;")
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        self.setStyleSheet(f"background: {self._background_colour}; border: {self._orig_border_width}px solid black;")

class ToolBar(QToolBar):
    def __init__(self, window, icon_size, background_colour, font_family, font_size):

        super().__init__(window)

        self._orig_icon_size = icon_size
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setIconSize(icon_size)
        self.setStyleSheet(f"background : {background_colour}")
    
    def maximise(self, factor):
        self.setIconSize(icon_size := QSize(int(self._orig_icon_size.width() * factor), int(self._orig_icon_size.height() * factor)))
        for widget in self.children():
            if isinstance(widget, MenuButton):
                widget.menu.setFont(QFont(self._font_family, int(self._orig_font_size * factor)))
                widget.setIconSize(icon_size)
    
    def minimise(self):
        self.setIconSize(self._orig_icon_size)
        for widget in self.children():
            if isinstance(widget, MenuButton):
                widget.menu.setFont(QFont(self._font_family, self._orig_font_size))
                widget.setIconSize(self._orig_icon_size)

class LineEdit(QLineEdit):
    def __init__(self, window, x, y, width, height, font_family, font_size, text, password):

        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font_family, font_size))
        self.setPlaceholderText(text)
        if password:
            self.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))


class Screen(QMainWindow): # Screen
    def __init__(self, appearance_config : AppearanceConfiguration, max_size : QSize):
        super().__init__()
        self._widgets = []
        self._appearance_config = appearance_config
        self._max_size = max_size
        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))
        if (bg := appearance_config.background_colour) != "default":
            self.setStyleSheet(f"background: {bg};")
        self.statusBar().setFont(QFont(self._appearance_config.regular_font, 14))
        self.statusBar().setStyleSheet("color : red;")
        self._resize_factor = self._max_size.width() / self.minimumSize().width()
    
    def resizeEvent(self, event):
        factor = event.size().width() / self.minimumSize().width()
        if not self.isMaximized():
            for widget in self._widgets:
                widget.maximise(factor)
        elif factor == 1:
            for widget in self._widgets:
                widget.minimise()
    
    def initShowMaximised(self):
        self.showMaximized()
        for widget in self._widgets:
            widget.maximise(self._resize_factor)
    
    def manualMaximise(self):
        if self.isMaximized():
            for widget in self._widgets:
                widget.maximise(self._resize_factor)
    
    def show_error(self, err):
        self.statusBar().showMessage(str(err.args[0]))
        
class HomeScreen(Screen):

    play_singleplayer_signal = pyqtSignal()
    create_new_account_signal = pyqtSignal()
    sign_in_singal = pyqtSignal()
    sign_out_signal = pyqtSignal()
    view_stats_signal = pyqtSignal()
    customise_gui_signal = pyqtSignal()
    help_signal = pyqtSignal()

    def __init__(self, appearance_config, max_size, account):

        super().__init__(appearance_config, max_size)

        self.__account = account

        self.__title = Label(self, "S U D O K U", 0, 75, 1000, 100, self._appearance_config.title_font, 70)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__title.setStyleSheet("background: transparent;")

        self.__play_singleplayer_button = Button(self, "PLAY SINGLEPLAYER", 300, 250, 400, 50, self._appearance_config.regular_font, 25, self.__play_singleplayer)
        self.__play_singleplayer_button.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

        self.__play_multiplayer_button = Button(self, "PLAY MULTIPLAYER", 300, 320, 400, 50, self._appearance_config.regular_font, 25, None)
        self.__play_multiplayer_button.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

        self.__leaderboard_button = Button(self, "LEADERBOARD", 300, 390, 400, 50, self._appearance_config.regular_font, 25, None)
        self.__leaderboard_button.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

        self.__toolbar = ToolBar(self, size := QSize(60, 60), self._appearance_config.colour3, font_family := self._appearance_config.regular_font, font_size := 15)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.__toolbar)
        self.__toolbar.addAction(Action(self, QIcon("resources/exit.svg"), "Quit", self.__quit_game, False))
        if self.__account is None:
            options = [("Create Account", self.__create_new_account), ("Sign In", self.__sign_in)]
        else:
            options = [("Create Account", self.__create_new_account), ("Sign Out", self.__sign_out), ("Show Stats", self.__view_stats),]
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/account.svg"), size, QFont(font_family, font_size), options))
        self.__toolbar.addWidget(MenuButton(self, QIcon("resources/settings.svg"), size, QFont(font_family, font_size), 
                                     [("Customise GUI", self.__customise_gui), ("Manage Account", None)]))
        self.__toolbar.addAction(Action(self, QIcon("resources/help.svg"), "Help", self.__help_screen, False))

        self.__account_label = Label(self, "Not Signed In" if self.__account is None else f"Signed in as {self.__account}", 
                                     0, 0, 300, 50, self._appearance_config.regular_font, 15)

        self._widgets += [self.__title, self.__play_singleplayer_button, self.__play_multiplayer_button, self.__leaderboard_button, self.__toolbar, self.__account_label]

    def __play_singleplayer(self):
        self.play_singleplayer_signal.emit()
    
    def __create_new_account(self):
        self.create_new_account_signal.emit()
    
    def __sign_in(self):
        self.sign_in_singal.emit()
    
    def __sign_out(self):
        self.sign_out_signal.emit()

    def __view_stats(self):
        if self.__account is None:
            self.statusBar().showMessage("Please sign in to view stats")
        else:
            self.view_stats_signal.emit()
    
    def __customise_gui(self):
        self.customise_gui_signal.emit()
    
    def __help_screen(self):
        self.help_signal.emit()

    def __quit_game(self):
        exit()

class OpenOrCreateNewGameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    create_new_game_signal = pyqtSignal()
    open_game_signal = pyqtSignal()

    def __init__(self, appearance_config, max_size, account):

        super().__init__(appearance_config, max_size)

        self.__account = account

        self.__open_game_button = Button(self, "OPEN EXISTING GAME", 70, 80, 400, 400, self._appearance_config.regular_font, 25, self.__open_game)
        self.__open_game_button.setStyleSheet(f"background: {self._appearance_config.colour4}; border: 5px solid black;")
        self.__create_new_game_button = Button(self, "CREATE NEW GAME", 530, 80, 400, 400, self._appearance_config.regular_font, 25, self.__create_new_game)
        self.__create_new_game_button.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 5px solid black;")

        self.__back_button = BackButton(self, self.__return_to_home_screen)

        self._widgets += [self.__open_game_button, self.__create_new_game_button, self.__back_button]
    
    def __open_game(self):
        if self.__account is not None:
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

    def __init__(self, appearance_config, max_size, account):

        super().__init__(appearance_config, max_size)

        self.__account = account

        self.__title = Label(self, "OPEN EXISTING GAME", 0, 25, 1000, 100, self._appearance_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, self._appearance_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__choose_game = Label(self, "CHOOSE A GAME: ", 50, 150, 300, 100, self._appearance_config.regular_font, 20)
        self.__choose_game_menu = ComboBox(self, 50, 230, 400, 50,self._appearance_config.regular_font, 15, 
                                           os.listdir(os.path.join(Game.DEFAULT_DIRECTORY, self.__account)) if self.__account is not None else [])
        self.__choose_game_menu.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__choose_game_menu.activated.connect(self.__show_game_info)

        self.statusBar().setFont(QFont(self._appearance_config.regular_font, 14))
        self.statusBar().setStyleSheet("QStatusBar{color:red;}")

        self.__game_info = TextEdit(self, 50, 300, 400, 235, self._appearance_config.colour2,  2, self._appearance_config.regular_font, 18)

        self._widgets += [self.__title, self.__play, self.__back, self.__choose_game, self.__choose_game_menu, self.__game_info]
    
    def __show_game_info(self):
        if file := self.__choose_game_menu.currentText():
            stats = Game.get_stats_from(os.path.join(self.__account, file))
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

    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)

        self.__title = Label(self, "CREATE NEW GAME", 0, 25, 1000, 100, self._appearance_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__play = Button(self, "PLAY GAME", 675, 290, 200, 50, self._appearance_config.regular_font, 20, self.__play_game)
        self.__play.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__mode = Label(self, "MODE: ", 50, 150, 300, 100, self._appearance_config.regular_font, 24)
        self.__difficulty = Label(self, "DIFFICULTY: ", 50, 225, 300, 100, self._appearance_config.regular_font, 24)
        self.__timed = Label(self, "TIMED: ", 50, 300, 300, 100, self._appearance_config.regular_font, 24)
        self.__board_size = Label(self, "BOARD SIZE: ", 50, 375, 300, 100, self._appearance_config.regular_font, 24)

        self.__mode_menu = ComboBox(self, 330, 175, 200, 50, self._appearance_config.regular_font, 20, ["Normal", "Killer"])
        self.__mode_menu.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__difficulty_menu = ComboBox(self, 330, 250, 200, 50, self._appearance_config.regular_font, 20, ["Easy", "Medium", "Hard", "Expert"])
        self.__difficulty_menu.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__timed_menu = ComboBox(self, 330, 325, 200, 50, self._appearance_config.regular_font, 20, ["Yes", "No"])
        self.__timed_menu.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
        self.__board_size_menu = ComboBox(self, 330, 400, 200, 50, self._appearance_config.regular_font, 20, ["4x4", "6x6", "9x9", "12x12", "16x16"])
        self.__board_size_menu.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__play, self.__back, self.__mode, self.__difficulty, self.__timed, self.__board_size,
                          self.__mode_menu, self.__difficulty_menu, self.__timed_menu, self.__board_size_menu]

    def __play_game(self):
        if (difficulty := self.__difficulty_menu.currentText()) and (timed := self.__timed_menu.currentText()) and \
            (board_size := self.__board_size_menu.currentText()) and (mode := self.__mode_menu.currentText()):
            if board_size == "16x16" and difficulty == "Expert":
                self.statusBar().showMessage("*16x16 Expert is not available")
            else:
                self.setWindowTitle("Board Generation in Progress")
                self.play_game_signal.emit([mode, difficulty, int(board_size.split("x")[0]), True if timed == "Yes" else False])
        else:
            self.statusBar().showMessage("*To continue, please fill all boxes")

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GameScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    PADDING, STARTX = 25, 10
    NUM_FONT_SIZES = {4: 20*9 // 4, 6: 20*9 // 6, 9: 20, 12: 20 * 9 // 12, 16: 20*9 // 16}
    HINT_FONT_SIZES = {4: 13*9 // 4, 6: 13*9 // 6, 9: 13, 12: 13 * 9 // 12, 16: 5}
    TOTAL_FONT_SIZES = {4: 10*9 // 4, 6: 10*9 // 6, 9: 10, 12: 10 * 9 // 12, 16: 10 * 9 // 16}

    def __init__(self, appearance_config, max_size, account):
        
        super().__init__(appearance_config, max_size)

        self.__selected_square = (None, None)
        self.__notes_mode = False
        self.__running = True
        self.__account = account

        self.__timer = Button(self, "", 610, 20, 130, 65, self._appearance_config.regular_font, 21, self.__pause_game)
        self.__timer.setStyleSheet("border: 2px solid black;")
        self.__progress = ProgressBar(self, 610, 110, 330, 20)
        self.__progress.setStyleSheet("QProgressBar::chunk{background-color: #99d9ea;}")

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.__info_label = Label(self, "", 595, 15, 310, 90, self._appearance_config.regular_font, 14)
        self.__info_label.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black; border-radius: 30px;")
        self.__info_label.hide()
        self.__info_button = CircularButton(self, 845, 15, 60, 60, QIcon("resources/info.svg"), self.__toggle_info_screen)

        self.__undo_button = CircularButton(self, 610, 470, 58, 58, QIcon("resources/undo.svg"), self.__undo_move)
        self.__delete_button = CircularButton(self, 677, 470, 58, 58, QIcon("resources/delete.svg"), self.__remove_num)
        self.__delete_button.setIconSize(QSize(53, 53))
        self.__delete_button.setStyleSheet("border-radius: 29px; border: 5px solid black;")
        self.__hint_button = CircularButton(self, 744, 470, 58, 58, QIcon("resources/hint.svg"), self.__show_hint)
        self.__num_hints_label = Label(self, "", 748, 535, 58, 58, self._appearance_config.regular_font, 15)
        self.__num_hints_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__notes_button = CircularButton(self, 811, 470, 58, 58, QIcon("resources/notes_off.svg"), self.__toggle_notes_mode)
        self.__notes_button.setIconSize(QSize(53, 53))
        self.__notes_button.setStyleSheet("border-radius: 29px; border: 5px solid black;")
        self.__resign_button = CircularButton(self, 878, 470, 58, 58, QIcon("resources/resign.svg"), partial(self.__show_end_screen, False))

        self._widgets += [self.__timer, self.__back, self.__info_label, self.__info_button, self.__undo_button, 
                          self.__delete_button, self.__hint_button, self.__num_hints_label, self.__notes_button, 
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
        self.__info_label.setText(f"Mode: {self.__game.mode} \nDifficulty: {self.__game.difficulty} \nBoard Size: {self.__game.board_size}x{self.__game.board_size} \nTimed: {self.__game.timed}")
        self.__num_hints_label.setText(str(self.__game.num_hints_left))

        if self.__game.mode == "Killer":
            self.__colours = self.__game.group_colours

        self.__create_curr_grid()
        self.__progress.setValue(int(self.__game.percent_complete()))

        self.__board_cover = Rect(self, self.STARTX+self.PADDING-3, self.PADDING-3, width:= self.GRIDSIZE*self.__game.board_size+12, height := self.GRIDSIZE*self.__game.board_size+12,
                                  self._appearance_config.colour2, 5)

        self.__paused_label = Label(self.__board_cover, "GAME PAUSED", 0, 0, width, height, self._appearance_config.regular_font, 24)
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
                                   self._appearance_config.regular_font, 20, partial(self.__place_num, num))
                num_input.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")
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
                                font_family = self._appearance_config.regular_font,
                                font_size = self.__num_font_size if sq.num != 0 else self.__hint_font_size, 
                                command = partial(self.__select_square, row+1, col+1))
                square.setFont(QFont(self._appearance_config.regular_font, self.__num_font_size if sq.num != 0 else self.__hint_font_size))
                square.setStyleSheet(f"border: {5 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + 
                                     (("#99d9ea" if self.__game.mode == "Normal" else "#C8C8C8") if (row+1, col+1) == self.__selected_square else ("white" if self.__game.mode == 'Normal' else self._appearance_config.killer_colours[self.__colours[(row, col)]])) + 
                                     ";color:" + ("black" if orig_board[row][col].num != 0 else ("blue" if sq.num != 0 else "red")) + 
                                     (";text-align: left" if sq.num == 0 else "") + 
                                     ";")
                self.__sqrs[row][col] = square
                self._widgets.append(square)
                square.show()  

                if self.__game.mode == "Killer" and (row, col) in self.__game.groups:
                    total_label = Label(self, str(self.__game.groups[(row, col)][1]), square.x(), square.y(), square.width()//3, square.height()//3, self._appearance_config.regular_font, self.__total_font_size)
                    total_label.show()
                    self._widgets.append(total_label)

    def __update_number_grid(self, curr_board, orig_board):
        mult = self._resize_factor if self.isMaximized() else 1
        for row, row_lst in enumerate(self.__sqrs):
            for col, sq in enumerate(row_lst):
                sq.setText(str(num) if (num := to_letter(curr_board[row][col].num)) != "0" else self.__game.note_at(row, col))
                sq.setFont(QFont(self._appearance_config.regular_font, int(mult * (self.__num_font_size if num != "0" else self.__hint_font_size))))
                sq.setStyleSheet(f"border: {3 if (row+1, col+1) == self.__selected_square else 2}px solid black; background-color:" + 
                                     (("#99d9ea" if self.__game.mode == "Normal" else "#C8C8C8") if (row+1, col+1) == self.__selected_square else ("white" if self.__game.mode == 'Normal' else self._appearance_config.killer_colours[self.__colours[(row, col)]])) + 
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
        self.__game.remove_game_file()
        if self.__game.timed:
            self.__timer_event.stop()

        bg = Rect(self, 0, 0, 1000, 560, self._appearance_config.colour2_translucent, 0)
        bg.show()

        window = Rect(self, 200, 30, 600, 500, "white", 5)
        window.show()
    
        title = Label(self, "You Won!" if win else "Game Over!", 0, 50, 1000, 100, self._appearance_config.title_font, 40)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("background: transparent;")
        title.show()

        if self.__game.timed:

            time_label_top = Label(self, "Time Elapsed: ", 0, 160, 1000, 100, self._appearance_config.regular_font, 20)
            time_label_top.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time_label_top.setStyleSheet("background: transparent;")
            time_label_top.show()

            time = Label(self, self.__game.time_elapsed, 0, 200, 1000, 100, self._appearance_config.regular_font, 60)
            time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            time.setStyleSheet("background: transparent;")
            time.show()

        home_screen_button = Button(self, "RETURN TO HOME", 350, 450, 300, 50, self._appearance_config.regular_font, 20, self.__return_to_home_screen)
        home_screen_button.show()

        solution_button = Button(self, "SEE SOLUTION", 350, 390, 300, 50, self._appearance_config.regular_font, 20,self.__show_solution_screen)
        if not win:
            solution_button.show()
        
        self._widgets += [bg, window, title, time_label_top, time, home_screen_button, solution_button]

        self.manualMaximise()
    
    def __show_solution_screen(self):

        bg = Rect(self, 0, 0, 1000, 560, "white", 0)
        bg.show()
        
        self.__show_border(self.__game.board_size, self.__game.matrix_size)
        self.__create_solution_grid()

        home_screen_button = Button(self, "RETURN TO HOME", 625, 250, 300, 50, self._appearance_config.regular_font, 20, self.__return_to_home_screen)
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
                    self.__game.put_down_number(self.__selected_square[0], self.__selected_square[1], num)            
            except GameError as err:
                self.show_error(err)
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
                self.show_error(err)
            self.__update_curr_grid()
        else:
            self.__show_game_paused_error()
    
    def __show_hint(self):
        if self.__running:
            try:
                self.__game.add_hint_to_notes(self.__selected_square[0], self.__selected_square[1])
                self.__num_hints_label.setText(str(self.__game.num_hints_left))
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
        self.__timer.setStyleSheet(f"background: {'white' if self.__running else self._appearance_config.colour2}; border: 2px solid black;")
        self.__board_cover.setHidden(not self.__board_cover.isHidden())
        if self.__game.timed:
            if self.__running: self.__timer_event.start(10)
            else: self.__timer_event.stop()
    
    def __update_time_elapsed(self):
        self.__game.inc_time_elapsed()
        self.__timer.setText(str(self.__game.time_elapsed))

    def __return_to_home_screen(self):
        if self.__running and self.__account is not None: # game quit from the "back" button
            self.__game.save_game(self.__account)
        self.return_to_home_screen_signal.emit()

class CreateNewAccountScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    create_account_signal = pyqtSignal(list)
    
    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)

        self.__title = Label(self, "CREATE NEW ACCOUNT", 0, 25, 1000, 100, self._appearance_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__username = LineEdit(self, 400, 200, 500, 50, self._appearance_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._appearance_config.regular_font, 20)

        self.__password = LineEdit(self, 400, 300, 500, 50, self._appearance_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._appearance_config.regular_font, 20)

        self.__password2 = LineEdit(self, 400, 400, 500, 50, self._appearance_config.regular_font, 15, "Type here: ", True)
        self.__password_label2 = Label(self, "Enter password again: ", 100, 400, 300, 50, self._appearance_config.regular_font, 20)

        self.__create = Button(self, "Create", 400, 500, 200, 50, self._appearance_config.regular_font, 20, self.__create_account)
        self.__create.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

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
    
    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)

        self.__title = Label(self, "SIGN IN", 0, 25, 1000, 100, self._appearance_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self.__username = LineEdit(self, 400, 200, 500, 50, self._appearance_config.regular_font, 15, "Type here: ", False)
        self.__username_label = Label(self, "Username: ", 100, 200, 300, 50, self._appearance_config.regular_font, 20)

        self.__password = LineEdit(self, 400, 300, 500, 50, self._appearance_config.regular_font, 15, "Type here: ", True)
        self.__password_label = Label(self, "Password: ", 100, 300, 300, 50, self._appearance_config.regular_font, 20)

        self.__sign_in = Button(self, "Sign In", 400, 400, 200, 50, self._appearance_config.regular_font, 20, self.__sign_in)
        self.__sign_in.setStyleSheet(f"background: {self._appearance_config.colour2}; border: 2px solid black;")

        self._widgets += [self.__title, self.__back, self.__username, self.__username_label, self.__password, 
                          self.__password_label, self.__sign_in]
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()
    
    def __sign_in(self):
        if self.__username.text() and self.__password.text():
            self.sign_in_signal.emit([self.__username.text(), self.__password.text()])
        else:
            self.statusBar().showMessage("One or more input boxes are still empty")


class ViewStatsScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()
    
    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self._widgets += [self.__back]
    
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class CustomiseGUIScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)
        
        self.__title = Label(self, "CUSTOMISE GUI", 0, 25, 1000, 100, self._appearance_config.title_font, 50)
        self.__title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__back = BackButton(self, self.__return_to_home_screen)

        self._widgets += [self.__title, self.__back]

    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class HelpScreen(Screen):

    return_to_home_screen_signal = pyqtSignal()

    def __init__(self, appearance_config, max_size):

        super().__init__(appearance_config, max_size)

        self.__back = BackButton(self, self.__return_to_home_screen)
        self.setStyleSheet(f"background: {self._appearance_config.colour3};")

        self.__txt_window = TextEdit(self, 100, 20, 800, 520, "white", 5, self._appearance_config.regular_font, 20)
        self.__txt_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        with open("resources/help.txt", "r") as f:
            self.__txt_window.insertPlainText(f.read())

        self._widgets += [self.__back, self.__txt_window]
        
    def __return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

class GUI(UI):

    def __init__(self):

        super().__init__()

        self.__account = None

        self.__app = QApplication(argv)
        self.__max_size = self.__app.primaryScreen().size()

        with open("options.json") as f:
            self.__options = json.load(f)

        QFontDatabase.addApplicationFont("resources/library-3-am.3amsoft.otf")
        QFontDatabase.addApplicationFont("resources/Metropolis-Regular.otf")

        self.__appearance_config = AppearanceConfiguration()

        self.__screens = {"home": self.__home_screen(), "open or create new game": self.__open_or_create_new_game_screen(),
                           "config game": self.__config_game_screen(), "open game": self.__open_game_screen(),
                           "game": self.__game_screen(), "create new account": self.__create_new_account_screen(), 
                           "sign in": self.__sign_in_screen(), "view stats": self.__view_stats_screen(),
                           "customise gui": self.__customise_gui_screen(), "help": self.__help_screen()}

        self.__screen_partials = {"home": self.__home_screen, "open or create new game": self.__open_or_create_new_game_screen,
                           "config game": self.__config_game_screen, "open game": self.__open_game_screen,
                           "game": self.__game_screen, "create new account": self.__create_new_account_screen, 
                           "sign in": self.__sign_in_screen, "view stats": self.__view_stats_screen,
                           "customise gui": self.__customise_gui_screen, "help": self.__help_screen}


        self.__show_curr_screen()
    
    def __home_screen(self):
        home_screen = HomeScreen(self.__appearance_config, self.__max_size, self.__account)
        home_screen.play_singleplayer_signal.connect(partial(self.__show_screen, "open or create new game", self.__open_or_create_new_game_screen))
        home_screen.create_new_account_signal.connect(partial(self.__show_screen, "create new account", self.__create_new_account_screen))
        home_screen.sign_in_singal.connect(partial(self.__show_screen, "sign in", self.__sign_in_screen))
        home_screen.sign_out_signal.connect(self.__sign_out)
        home_screen.view_stats_signal.connect(partial(self.__show_screen, "view stats", self.__view_stats_screen))
        home_screen.customise_gui_signal.connect(partial(self.__show_screen, "customise gui", self.__customise_gui_screen))
        home_screen.help_signal.connect(partial(self.__show_screen, "help", self.__help_screen))
        return home_screen
    
    def __open_or_create_new_game_screen(self):
        open_or_create_new_game_screen = OpenOrCreateNewGameScreen(self.__appearance_config, self.__max_size, self.__account)
        open_or_create_new_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_or_create_new_game_screen.open_game_signal.connect(partial(self.__show_screen, "open game", self.__open_game_screen))
        open_or_create_new_game_screen.create_new_game_signal.connect(partial(self.__show_screen, "config game", self.__config_game_screen))  
        return open_or_create_new_game_screen
    
    def __open_game_screen(self):
        open_game_screen = OpenGameScreen(self.__appearance_config, self.__max_size, self.__account)
        open_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        open_game_screen.play_game_signal.connect(self.__load_game_screen)
        return open_game_screen

    def __config_game_screen(self):
        config_game_screen = ConfigGameScreen(self.__appearance_config, self.__max_size)
        config_game_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        config_game_screen.play_game_signal.connect(self.__show_game_screen)
        return config_game_screen

    def __game_screen(self):
        game_screen = GameScreen(self.__appearance_config, self.__max_size, self.__account)
        game_screen.return_to_home_screen_signal.connect(self.__quit_game)
        return game_screen

    def __create_new_account_screen(self):
        create_new_account_screen = CreateNewAccountScreen(self.__appearance_config, self.__max_size)
        create_new_account_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        create_new_account_screen.create_account_signal.connect(self.__create_account)
        return create_new_account_screen

    def __sign_in_screen(self):
        sign_in_screen = SignInScreen(self.__appearance_config, self.__max_size)
        sign_in_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        sign_in_screen.sign_in_signal.connect(self.__sign_in)
        return sign_in_screen
    
    def __view_stats_screen(self):
        view_stats_screen = ViewStatsScreen(self.__appearance_config, self.__max_size)
        view_stats_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return view_stats_screen
    
    def __customise_gui_screen(self):
        customise_gui_screen = CustomiseGUIScreen(self.__appearance_config, self.__max_size)
        customise_gui_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return customise_gui_screen

    def __help_screen(self):
        help_screen = HelpScreen(self.__appearance_config, self.__max_size)
        help_screen.return_to_home_screen_signal.connect(self.__pop_screen)
        return help_screen

    def __close_curr_screen(self):
        self.__screens[self._get_curr_ui()].close()
    
    def __show_curr_screen(self):
        if self.__options["full screen"]:
            self.__screens[self._get_curr_ui()].initShowMaximised()
        else:
            self.__screens[self._get_curr_ui()].show()
   
    def __push_screen(self, screen):
        self.__close_curr_screen()
        self._push_ui_to_stack(screen)
        self.__show_curr_screen()
        
    def __pop_screen(self):
        self.__close_curr_screen()
        self._pop_ui_from_stack()
        self.__screens[ui] = self.__screen_partials[ui := self._get_curr_ui()]()
        self.__show_curr_screen()
    
    def __show_screen(self, screen_name, screen_func):
        self.__screens[screen_name] = screen_func()
        self.__push_screen(screen_name)
    
    def __show_game_screen(self, options):
        mode, difficulty, board_size, timed = options
        self.__game = Game()
        self.__game.generate(mode, difficulty, board_size, timed)
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __load_game_screen(self, file):
        self.__game = Game()
        self.__game.load_game(os.path.join(self.__account, file))
        self.__screens["game"] = self.__game_screen()
        self.__screens["game"].set_game(self.__game)
        self.__push_screen("game")
    
    def __create_account(self, options):
        try:
            username, password = options
            database.create_new_account(username, password)
            os.mkdir(os.path.join(Game.DEFAULT_DIRECTORY, f"{username}"))
            self.__account = username
            self.__pop_screen()
        except DBError as err:
            self.__screens["create new account"].show_error(err)
    
    def __sign_in(self, options):
        try:
            username, password = options
            if not database.password_at(username):
                raise DBError("Username doesn't exist")
            if database.password_at(username)[0][0] == database.encrypt_password(password):
                self.__account = username
                print(f"Signed In as {username}")
            else:
                raise DBError("Incorrect Password")
            self.__pop_screen()
        except DBError as err:
            self.__screens["sign in"].show_error(err)
    
    def __sign_out(self):
        self.__account = None
        print("Signed Out")
        self.__close_curr_screen()
        self.__show_screen("home", self.__screen_partials["home"])
            
    def __quit_game(self):
        self.__close_curr_screen()
        for _ in range(3):
            self._pop_ui_from_stack()
        self.__show_curr_screen()

    def run(self):
        exit(self.__app.exec())
