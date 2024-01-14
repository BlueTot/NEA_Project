import os # Import os library
from account import * # Import everything from account.py file
from rating_calc import get_title, RECOMMENDED_RATINGS, average_time_to_complete # import functions from rating calculation file
from database import * # Import all database functions

class ApplicationError(Exception):
    pass

class Application: # Application class, used to manage accounts and all account-related features

    DEFAULT_DIRECTORY = "games" # Default directory to store game files

    def __init__(self): # Constructor
        self.__account = Account() # Create account
    
    @property
    def account(self): # Get account
        return self.__account
    
    @property
    def signed_in(self): # Get signed in or not
        return self.__account.username is not None
    
    def get_game_files(self): # Get list of game file names
        if self.signed_in:
            return os.listdir(os.path.join(self.DEFAULT_DIRECTORY, self.__account.username)) 
        return []

    def create_account(self, options): # Method to create new account
        username, password = options
        database.create_new_account(username, password) # Create new account in database
        os.mkdir(os.path.join(self.DEFAULT_DIRECTORY, f"{username}")) # Create new directory for stored games
        self.__account.set_account(username) # Set the account in the GUI
    
    def check_password_match(self, password):
        return database.encrypt_password(password) == database.password_at(self.__account.username)[0][0]
    
    def sign_in(self, options): # Method to sign in
        username, password = options
        if not database.password_at(username): # Username does not exist
            raise DBError("Username doesn't exist")
        if database.password_at(username)[0][0] == database.encrypt_password(password): # Check if password entered is correct
            self.__account.set_account(username) # Set account
            print(f"Signed In as {username}")
        else:
            raise DBError("Incorrect Password")

    def sign_out(self): # Method to sign out
        self.__account.set_account(None)
        print("Signed Out")
    
    def get_preset(self, preset_num):
        try:
            return database.get_preset(self.__account.username, preset_num)
        except IndexError:
            return database.get_preset(self.__account.username, 1)
    
    def use_gui_preset(self, preset_num): # Method to use certain appearance preset (from view gui preset screen)
        database.set_current_appearance_preset(self.__account.username, preset_num)
        self.__account.update_app_config()
    
    def update_appearance_preset(self, options): # Method to update appearance preset (from edit gui preset screen)
        mode, preset_num, data = options[0], options[1], options[2:]
        if mode == "edit": # Edit existing preset
            database.update_appearance_preset(self.__account.username, preset_num, data)
        else: # Create new preset
            database.create_new_appearance_preset(self.__account.username, data)
        self.__account.update_app_config()

    def delete_appearance_preset(self, preset_num): # Method to reset appearance preset (from edit gui preset screen)
        database.delete_appearance_preset(self.__account.username, preset_num)
        self.__account.update_app_config()
    
    def save_game_stats(self, data): # Method to save game stats after each game
        database.add_game(self.__account.username, data)
    
    def change_username(self, new_username): # Method to change username (from manage account screen)
        database.change_username(self.__account.username, new_username)
        os.rename(os.path.join(self.DEFAULT_DIRECTORY, f"{self.__account.username}"), 
                  os.path.join(self.DEFAULT_DIRECTORY, f"{new_username}"))
        self.__account.set_account(new_username)

    def change_password(self, password): # Method to change password (from manage account screen)
        database.change_password(self.__account.username, password)
    
    def delete_account(self): # Method to delete account (from manage account screen)
        database.delete_account(self.__account.username)
        os.rmdir(os.path.join(self.DEFAULT_DIRECTORY, f"{self.__account.username}"))
        self.__account.set_account(None)
    
    def update_rating(self, rating_change): # Method to update singleplayer rating (after each game)
        new_rating = self.__account.rating + rating_change
        if new_rating >= 0:
            new_title = get_title(new_rating)
            database.update_rating_and_title(self.__account.username, new_rating, new_title)
            self.__account.update_rating()
            self.__account.update_title()
    
    def __curr_milestone_rank(self, milestone): # Method to get current milestone rank (1 to 7) of any milestone collection
        for rank, comps in reversed(GameMilestones.MILESTONES.items()):
            if milestone >= comps:
                return rank
        else:
            return 0
    
    def update_milestone(self, data): # Method to update milestone after each game

        mode, board_size, difficulty, won = data

        if won: # Check if user has won the game

            milestone = database.milestone(self.__account.username, bs := f"milestone_{board_size}x{board_size}") # get current milestone
            new_milestone = milestone + GameMilestones.MILESTONE_GAIN[difficulty] * (2 if mode == "Killer" else 1) # Calculate new milestone
            database.set_milestone(self.__account.username, bs, new_milestone) # Update to database

            old_rank = self.__curr_milestone_rank(milestone) # Calculate old milestone rank
            new_rank = self.__curr_milestone_rank(new_milestone) # Calculate new milestone rank

            if new_rank != old_rank: # Check if milestone rank changed
                claimed = database.milestone_claimed(self.__account.username) # Get claimed string
                idx = GameMilestones.BOARD_SIZE_IDXS[board_size] * 7 + new_rank - 1 # Get index to update
                database.set_milestone_claimed(self.__account.username, claimed[:idx] + "1" + claimed[idx+1:]) # Update the index to signify that a milestone reward needs to be claimed

            print(f"Milestone successfully updated for {self.__account.username}")
    
    def claim_reward(self, data): # Method to claim reward for a milestone (from game milestone screen)
        
        board_size, milestone_num = data
        claimed = database.milestone_claimed(self.__account.username) # Get claimed string
        idx = GameMilestones.BOARD_SIZE_IDXS[board_size] * 7 + milestone_num - 1 # Get index to update
        database.set_milestone_claimed(self.__account.username, claimed[:idx] + "0" + claimed[idx+1:]) # Update the index to claim reward
        reward = GameMilestones.REWARDS[f"{board_size}x{board_size}"][milestone_num] # Get the reward
        if reward is not None and reward[0] == "H":
            bonus_hints = database.bonus_hints(self.__account.username)
            database.set_bonus_hints(self.__account.username, bonus_hints + reward[1]) # Add the bonus hints earned from the reward
        
        print(f"Milestone reward claimed")
    
    @staticmethod
    def get_recommended_rating(mode, board_size, difficulty):
        return RECOMMENDED_RATINGS[(mode, int(board_size.split("x")[0]), difficulty)]
    
    @staticmethod
    def get_average_time_to_complete(mode, board_size, difficulty):
        return average_time_to_complete(mode, int(board_size.split("x")[0]), difficulty)
        