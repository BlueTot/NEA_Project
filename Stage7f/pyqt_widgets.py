from ui import UI # Import UI for the version number

'''PyQt GUI Imports'''

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QToolBar, QMenu, QComboBox, QProgressBar, QWidget, QTextEdit, QLineEdit, QTableWidget, QAbstractScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView

class Button(QPushButton): # Screen Button

    def __init__(self, window, text, x, y, width, height, font_family, font_size, command): # Constructor
        super().__init__(text, window) # Inheritance

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
        super().__init__(window) # Inheritance

        # Store original dimensions and coordinates
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._orig_border_width = border_width

        # Set size and style sheet
        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"border: {border_width}px solid black;")
    
    # Scale up border object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        self.setStyleSheet(f"border: {int(self._orig_border_width*factor)}px solid black;")
    
    # Return border object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        self.setStyleSheet(f"border: {self._orig_border_width}px solid black;")

class Action(QAction): # Action for toolbar
    def __init__(self, window, image, text, command, checkable):
        if image is None: # Inheritance without image
            super().__init__(text, window)
        else: # Inheritance with image
            super().__init__(image, text, window)
        self.setCheckable(checkable)
        if command is not None: # Connect action to command if there is one
            self.triggered.connect(command)

class MenuButton(QPushButton): # Menu in a button for toolbar
    def __init__(self, window, icon, size, font, actions):
        super().__init__(window) # Inheritance
        self.setIcon(icon) # Set the icon (QIcon)
        self.setIconSize(size) # Set icon size (QSize)
        self.menu = QMenu() # Create menu in button
        if font is not None: # Set the font if there is one
            self.menu.setFont(font)
        for action, command in actions: # Loop through commands
            self.menu.addAction(Action(self, None, action, command, False)) # Add command / action to menu
        self.setMenu(self.menu) # Assign menu to button
        self.setStyleSheet("QPushButton::menu-indicator {width:0px;}") # Remove drop down arrow on the right

class Label(QLabel): # Screen label
    def __init__(self, window, text, x, y, width, height, font_family, font_size):
        super().__init__(window) # Inheritance

        # Store original dimensions and font size
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setText(text) # Set text
        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setFont(QFont(font_family, font_size)) # Set font
    
    # Scale up label object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    # Return label object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class ComboBox(QComboBox): # Screen ComboBox to input data
    def __init__(self, window, x, y, width, height, font_family, font_size, options, add_blank=True):
        super().__init__(window) # Inheritance

        # Store original dimensions
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setFont(QFont(font_family, font_size)) # Set font
        if add_blank: # Add a blank option if needed
            self.addItem("")
        self.addItems(options) # Add options
    
    # Scale up combo box object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class ProgressBar(QProgressBar): # Progress bar to display game progress
    def __init__(self, window, x, y, width, height):
        super().__init__(window) # Inheritance

        # Store original dimensions
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height

        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setTextVisible(True) # Set percentage number visible on progress bar
        self.setValue(0) # Set initial percentage value to 0
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)

class CircularButton(Button): # Screen button that is circular and has a border
    def __init__(self, window, x, y, width, height, image, command):
        super().__init__(window, "", x, y, width, height, None, None, command) # Inheritance
        self.setIcon(image) # Set icon
        self.setIconSize(QSize(width, height)) # Set size
        self.setStyleSheet("border-radius:" + str(width//2) + "px;") # Set border radius that depends on width
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        super().maximise(factor)
        self.setIconSize(QSize(int(self._orig_width*factor), int(self._orig_height*factor)))
        self.setStyleSheet("border-radius:" + str(self._orig_width*factor//2) + "px;")
    
    # Return object to original size when screen is minimised
    def minimise(self):
        super().minimise()
        self.setIconSize(QSize(self._orig_width, self._orig_height))
        self.setStyleSheet("border-radius:" + str(self._orig_width//2) + "px;")
    
class BackButton(CircularButton): # Back button to return to previous page
    def __init__(self, window, command):
        super().__init__(window, 925, 15, 60, 60, QIcon("resources/back.svg"), command) # Back button is just a circular button with an arrow image

class TextEdit(QTextEdit): # TextEdit object to display text, e.g. help menu and displaying contents of appearance preset / game files
    def __init__(self, window, x, y, width, height, background_colour, border_width, font_family, font_size):
        super().__init__(window) # Inheritance

        # Store original dimensions and font size
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setStyleSheet(f"background: {background_colour}; border: {border_width}px solid black;") # Set background colour and border width
        self.setFont(QFont(font_family, font_size)) # Set font
        self.setReadOnly(True) # Do not allow the reader to edit the text in the textedit
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class Rect(QWidget): # Rectangle with background colour widget
    def __init__(self, window, x, y, width, height, background_colour, border_width):
        super().__init__(window) # Inheritance

        # Store original dimensions and border width
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._background_colour = background_colour
        self._orig_border_width = border_width
        
        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setStyleSheet(f"background: {background_colour}; border: {border_width}px solid black;") # Set style sheet
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) # Allow background to have translucent colour
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        self.setStyleSheet(f"background: {self._background_colour}; border: {int(self._orig_border_width * factor)}px solid black;")
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        self.setStyleSheet(f"background: {self._background_colour}; border: {self._orig_border_width}px solid black;")

class ToolBar(QToolBar): # Toolbar widget
    def __init__(self, window, icon_size, background_colour, font_family, font_size):

        super().__init__(window) # Inheritance

        # Set original dimensions
        self._orig_icon_size = icon_size
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setIconSize(icon_size) # Set icon size (QSize)
        self.setStyleSheet(f"background : {background_colour}") # Set background colour
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setIconSize(icon_size := QSize(int(self._orig_icon_size.width() * factor), int(self._orig_icon_size.height() * factor)))
        for widget in self.children():
            if isinstance(widget, MenuButton):
                widget.menu.setFont(QFont(self._font_family, int(self._orig_font_size * factor)))
                widget.setIconSize(icon_size)
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setIconSize(self._orig_icon_size)
        for widget in self.children():
            if isinstance(widget, MenuButton):
                widget.menu.setFont(QFont(self._font_family, self._orig_font_size))
                widget.setIconSize(self._orig_icon_size)

class LineEdit(QLineEdit): # LineEdit widget used for user to enter username and password
    def __init__(self, window, x, y, width, height, font_family, font_size, text, password):

        super().__init__(window) # Inheritance

        # Store original dimensions
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setFont(QFont(font_family, font_size)) # Set font
        self.setStyleSheet("background: white; border: 2px solid black;") # Set background colour and border width
        self.setPlaceholderText(text) # Set placeholder text in grey
        if password: # Hide text typed if lineedit is used to input password
            self.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))

class TableWidget(QTableWidget): # Table widget, used to display rankings in leaderboard
    def __init__(self, window, x, y, width, height, font_family, font_size, background_colour, num_rows, num_cols):

        super().__init__(num_rows, num_cols, window) # Inheritance

        # Store original dimensions
        self._orig_x = x
        self._orig_y = y
        self._orig_width = width
        self._orig_height = height
        self._font_family = font_family
        self._orig_font_size = font_size

        self.setGeometry(x, y, width, height) # Set position and dimensions
        self.setStyleSheet(f"background: {background_colour};") # Set background colour
        self.setFont(QFont(font_family, font_size)) # Set font size
        self.horizontalHeader().setFont(QFont(font_family, font_size)) # Set font size of horizontal header
        self.verticalHeader().setFont(QFont(font_family, font_size)) # Set font size of vertical header
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Do not allow the user to edit the leaderboard table
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # Resize horizontal header columns to contents
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # Resize vertical header rows to contents
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents) # Resize cell size adjust to contents

    def load_data(self, headings, data): # Method to load table with data when given headings (list) and data (list[tuple])
        self.setSortingEnabled(False) # Disable sorting when loading data
        self.setColumnCount(len(headings)) # Set number of columns
        for row in range(self.rowCount()): # Loop through rows
            for col in range(self.columnCount()): # Loop through cols
                item = QTableWidgetItem() # Create table widget item
                value = data[row][col] if 0 <= row < len(data) and 0 <= col < len(data[0]) else "" # Get value if (row, col) in range
                item.setData(Qt.ItemDataRole.EditRole, value) # Assign value to item
                self.setItem(row, col, item) # Assign item to table
        self.setHorizontalHeaderLabels(headings) # Set horizontal column headers
        self.setSortingEnabled(True) # Enable sorting so user can click column headers to sort in ascending / descending order
        self.sortByColumn(1, Qt.SortOrder.DescendingOrder) # Sort ratings column (column 1) in descending order by default
    
    # Scale up object when screen is maximised
    def maximise(self, factor):
        self.setGeometry(int(self._orig_x*factor), int(self._orig_y*factor), int(self._orig_width*factor), int(self._orig_height*factor))
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, int(self._orig_font_size*factor)))
            self.horizontalHeader().setStyleSheet(ss := f"font-size: {self._orig_font_size*factor};")
            self.verticalHeader().setStyleSheet(ss)
    
    # Return object to original size when screen is minimised
    def minimise(self):
        self.setGeometry(self._orig_x, self._orig_y, self._orig_width, self._orig_height)
        if self._font_family is not None and self._orig_font_size is not None:
            self.setFont(QFont(self._font_family, self._orig_font_size))
            self.horizontalHeader().setStyleSheet(ss := f"font-size: {self._orig_font_size};")
            self.verticalHeader().setStyleSheet(ss)

class Screen(QMainWindow): # Screen widget, all GUI screens inherit from Screen

    return_to_home_screen_signal = pyqtSignal() 

    def __init__(self, application, max_size : QSize, title_name, create_button):
        super().__init__() # Inheritance
        self._widgets = [] # Initialise list of widgets to maximise / minimise
        self._application = application # Set application : Application
        self._max_size = max_size # Set max_size : QSize
        self.setWindowTitle(f"Sudoku {UI.VERSION}") # Set window title with version of game
        self.setMinimumSize(QSize(1000, 560)) # Set size of minimised window
        self.setStyleSheet(f"background: {self._application.account.app_config.background_colour};") # set background colour
        self.statusBar().setFont(QFont(self._application.account.app_config.regular_font, 14)) # Set font of status bar (to show errors)
        self.statusBar().setStyleSheet("color : red;") # Set colour of status bar (to show errors)
        self._resize_factor = self._max_size.width() / self.minimumSize().width() # Calculate resize factor for maximising
        if title_name is not None:
            self._title = Label(self, title_name, 0, 25, 1000, 100, self._application.account.app_config.title_font, 50)
            self._title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self._widgets.append(self._title)
        if create_button:
            self._back = BackButton(self, self._return_to_home_screen)
            self._widgets.append(self._back)
    
    # Method to return back to home screen
    def _return_to_home_screen(self):
        self.return_to_home_screen_signal.emit()

    # Override screen resize event (triggered on clicking maximise / minimise button)
    def resizeEvent(self, event):
        factor = event.size().width() / self.minimumSize().width() # Calculate factor
        if not self.isMaximized(): # If screen is not maximised
            for widget in self._widgets: # Loop through all widgets
                widget.maximise(factor) # Maximise the widget
        elif factor == 1: # If screen needs to be minimised
            for widget in self._widgets: # Loop through all widgets
                widget.minimise() # Minimise the widget
    
    # Show screen in maximised mode initally
    def initShowMaximised(self):
        self.showMaximized() # Maximise
        for widget in self._widgets: # Loop through all widgets
            widget.maximise(self._resize_factor) # Maximise the widget
    
    # Manually maximise widgets when widgets on screen are changed (e.g. in game end screen where user can see the solution)
    def manualMaximise(self):
        if self.isMaximized(): # Check if screen is already maximised
            for widget in self._widgets: # Loop through all widgets
                widget.maximise(self._resize_factor) # Maximise the widget
    
    def show_error(self, err): # Show error given Exception
        self.statusBar().showMessage(str(err.args[0])) # Show error in status bar
