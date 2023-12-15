from hex_to_dec import to_translucent # Import convert to translucent function
import database # Import database

class GameMilestones:

    MILESTONES = {1: 10, 2: 20, 3: 35, 4: 60, 5: 100, 6: 180, 7: 270}
    MILESTONE_GAIN = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}
    BOARD_SIZE_IDXS = {4: 0, 6: 1, 9: 2, 12: 3, 16: 4}
    REWARDS = {"4x4": {1: ("H", 1), 2: ("H", 2), 3: ("H", 4), 4: ("H", 6), 5: ("H", 9), 6: ("H", 15), 7: ("H", 21)},
               "6x6": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None},
               "9x9": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None},
               "12x12": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None},
               "16x16": {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}}

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
        self.__singleplayer_rating = None
        self.__singleplayer_title = None
        self.__app_config = app_config
    
    '''Getters'''
    
    @property
    def username(self):
        return self.__username
    
    @property
    def singleplayer_rating(self):
        return self.__singleplayer_rating
    
    @property
    def singleplayer_title(self):
        return self.__singleplayer_title
    
    @property
    def app_config(self):
        return self.__app_config
    
    def update_app_config(self):
        if self.__username is None:
            self.__app_config = AppearanceConfiguration(None)
        else:
            self.__app_config = AppearanceConfiguration(list(database.appearance_config_at(self.__username)[0]))
    
    def update_singleplayer_rating(self):
        if self.__username is None:
            self.__singleplayer_rating = None
        else:
            self.__singleplayer_rating = database.singleplayer_rating(self.__username)[0][0]
    
    def update_singleplayer_title(self):
        if self.__username is None:
            self.__singleplayer_title = None
        else:
            self.__singleplayer_title = database.singleplayer_title(self.__username)[0][0]
    
    def set_account(self, account):
        self.__username = account
        self.update_app_config()
        self.update_singleplayer_rating()
        self.update_singleplayer_title()