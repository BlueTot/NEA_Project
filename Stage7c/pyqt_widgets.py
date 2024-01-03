from ui import UI # Import UI for the version number

'''PyQt GUI Imports'''

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget, QTextEdit, QLineEdit, QTableWidget, QAbstractScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView

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
    def __init__(self, window, x, y, width, height, font_family, font_size, options, add_blank=True):
        super().__init__(window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height)
        self.setFont(QFont(font_family, font_size))
        if add_blank:
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
        self.setStyleSheet("background: white; border: 2px solid black;")
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

class TableWidget(QTableWidget):
    def __init__(self, window, x, y, width, height, font_family, font_size, background_colour, num_rows, num_cols):

        super().__init__(num_rows, num_cols, window)

        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"background: {background_colour};")
        self.setFont(QFont(font_family, font_size))
        self.horizontalHeader().setFont(QFont(font_family, font_size))
        self.verticalHeader().setFont(QFont(font_family, font_size))
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

    def load_data(self, headings, data):
        self.setSortingEnabled(False)
        self.setColumnCount(len(headings))
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = QTableWidgetItem()
                value = data[row][col] if 0 <= row < len(data) and 0 <= col < len(data[0]) else ""
                item.setData(Qt.ItemDataRole.EditRole, value)
                self.setItem(row, col, item)
        self.setHorizontalHeaderLabels(headings)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.SortOrder.DescendingOrder)
    
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
            self.horizontalHeader().setStyleSheet(ss := f"font-size: {self._orig_font_size*factor};")
            self.verticalHeader().setStyleSheet(ss)
            
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))
            self.horizontalHeader().setStyleSheet(ss := f"font-size: {self._orig_font_size};")
            self.verticalHeader().setStyleSheet(ss)

class Screen(QMainWindow): # Screen
    def __init__(self, application, max_size : QSize):
        super().__init__()
        self._widgets = []
        self._application = application
        self._max_size = max_size
        self.setWindowTitle(f"Sudoku {UI.VERSION}")
        self.setMinimumSize(QSize(1000, 560))
        self.setStyleSheet(f"background: {self._application.account.app_config.background_colour};")
        self.statusBar().setFont(QFont(self._application.account.app_config.regular_font, 14))
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