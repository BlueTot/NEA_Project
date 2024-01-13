from hex_to_dec import to_translucent # Import convert to translucent function
import database # Import database

class GameMilestones: # Game Milestones class

    MILESTONES = {1: 10, 2: 20, 3: 35, 4: 60, 5: 100, 6: 180, 7: 270} # Number of completions for each milestone dictionary
    MILESTONE_GAIN = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4} # Number of milestones gained after each run
    BOARD_SIZE_IDXS = {4: 0, 6: 1, 9: 2, 12: 3, 16: 4} # Indexes for board sizes
    REWARDS = {"4x4": {1: ("H", 1), 2: ("H", 2), 3: ("H", 4), 4: ("H", 6), 5: ("H", 9), 6: ("H", 14), 7: ("H", 20)},
               "6x6": {1: ("H", 2), 2: ("H", 3), 3: ("H", 5), 4: ("H", 7), 5: ("H", 11), 6: ("H", 16), 7: ("H", 22)},
               "9x9": {1: ("H", 3), 2: ("H", 5), 3: ("H", 8), 4: ("H", 11), 5: ("H", 14), 6: ("H", 18), 7: ("H", 24)},
               "12x12": {1: ("H", 4), 2: ("H", 6), 3: ("H", 9), 4: ("H", 13), 5: ("H", 16), 6: ("H", 19), 7: ("H", 26)},
               "16x16": {1: ("H", 5), 2: ("H", 8), 3: ("H", 11), 4: ("H", 15), 5: ("H", 19), 6: ("H", 24), 7: ("H", 30)}} # Hint rewards for each milestone

class AppearanceConfiguration: # Appearance Configuration class

    DEFAULT_SETTINGS = ['#f0f0f0', '#ffffff', '#aee8f5', '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 
                        'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3']

    def __init__(self, settings : list): # Constructor
        if settings is not None: # Signed In
            # Get colour settings from settings list
            self.__background_colour, self.__colour1, self.__colour2, self.__colour3, self.__colour4, self.__title_font, self.__regular_font = settings[:-5]
            self.__colour2_translucent = f"rgba{to_translucent(self.__colour2)}"
            self.__killer_colours = settings[-5:]
        else: # Not Signed In
            # Get colour settings from DEFAULT SETTINGS
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

    def __init__(self, username=None, app_config=AppearanceConfiguration(None)): # Constructor, set default username and appearance config upon login
        self.__username = username
        self.__rating = None
        self.__title = None
        self.__app_config = app_config
    
    '''Getters'''
    
    @property
    def username(self): # Get username
        return self.__username
    
    @property
    def rating(self): # Get rating
        return self.__rating
    
    @property
    def title(self): # Get title
        return self.__title
    
    @property
    def app_config(self): # Get appearance configuration
        return self.__app_config
    
    @property
    def app_preset_num(self):
        return database.get_current_appearance_preset_num(self.__username)
    
    @property
    def bonus_hints(self):
        return database.bonus_hints(self.__username)
    
    def update_app_config(self): # Update app config after preset changed
        if self.__username is None:
            self.__app_config = AppearanceConfiguration(None)
        else:
            self.__app_config = AppearanceConfiguration(list(database.appearance_config_at(self.__username)[0]))
    
    def update_rating(self): # Update rating after game
        if self.__username is None:
            self.__rating = None
        else:
            self.__rating = database.rating(self.__username)[0][0]
    
    def update_title(self): # Update title after game
        if self.__username is None:
            self.__title = None
        else:
            self.__title = database.title(self.__username)[0][0]
    
    def set_account(self, account): # Set account upon signing in
        self.__username = account
        self.update_app_config()
        self.update_rating()
        self.update_title()
        