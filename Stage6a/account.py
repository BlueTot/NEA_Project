from hex_to_dec import to_translucent # Import convert to translucent function
import database # Import database

class AppearanceConfiguration: # Appearance Configuration class

    DEFAULT_SETTINGS = ['#f0f0f0', '#ffffff', '#aee8f5', '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 
                        'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3']

    def __init__(self, settings): # Constructor
        if settings is not None:
            self.__background_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__title_font, self.__regular_font = settings[1:-5]
            self.__colour2_translucent = f"rgba{to_translucent(self.__colour2)}"
            self.__killer_colours = settings[-5:]
        else:
            self.__background_colour = self.DEFAULT_SETTINGS[0]
            self.__colour1 = self.DEFAULT_SETTINGS[1]
            self.__colour2 = self.DEFAULT_SETTINGS[2]
            self.__colour2_translucent = f"rgba{to_translucent(self.__colour2)}"
            self.__colour3 = self.DEFAULT_SETTINGS[3]
            self.__colour4 = self.DEFAULT_SETTINGS[4]
            self.__title_font = self.DEFAULT_SETTINGS[5]
            self.__regular_font = self.DEFAULT_SETTINGS[6]
            self.__killer_colours = self.DEFAULT_SETTINGS[7:] 
    
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

class Account: # Account Class

    def __init__(self, username=None, app_config=AppearanceConfiguration(None)):
        self.__username = username
        self.__app_config = app_config
    
    @property
    def username(self):
        return self.__username
    
    @property
    def app_config(self):
        return self.__app_config
    
    def update_app_config(self):
        if self.__username is None:
            self.__app_config = AppearanceConfiguration(None)
        else:
            self.__app_config = AppearanceConfiguration(list(database.appearance_config_at(self.__username)[0]))
    
    def set_account(self, account):
        self.__username = account
        self.update_app_config()