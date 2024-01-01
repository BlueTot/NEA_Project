import os
from account import *
from rating_calc import title
from database import *

class Application:

    DEFAULT_DIRECTORY = "games"

    def __init__(self):
        self.__account = Account()
    
    @property
    def account(self):
        return self.__account
    
    @property
    def games_directory(self):
        return f"{self.DEFAULT_DIRECTORY}/{self.__account.username}"

    def create_account(self, options): # Method to create new account
        username, password = options
        os.mkdir(os.path.join(self.DEFAULT_DIRECTORY, f"{username}")) # Create new directory for stored games
        database.create_new_account(username, password) # Create new account in database
        self.__account.set_account(username) # Set the account in the GUI
    
    def sign_in(self, options): # Method to sign in
        username, password = options
        if not database.password_at(username):
            raise DBError("Username doesn't exist")
        if database.password_at(username)[0][0] == database.encrypt_password(password):
            self.__account.set_account(username)
            print(f"Signed In as {username}")
        else:
            raise DBError("Incorrect Password")

    def sign_out(self): # Method to sign out
        self.__account.set_account(None)
        print("Signed Out")
    
    def update_appearance_config(self, options): # Method to update appearance config (from customise gui screen)
        database.update_appearance_config(self.__account.username, options)
        self.__account.update_app_config()

    def reset_appearance_config(self): # Method to reset appearance config (from customise gui screen)
        database.update_appearance_config(self.__account.username, AppearanceConfiguration.DEFAULT_SETTINGS)
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
    
    def update_singleplayer_rating(self, rating_change): # Method to update singleplayer rating (after each game)
        new_rating = self.__account.singleplayer_rating + rating_change
        if new_rating >= 0:
            new_title = title(new_rating)
            database.update_singleplayer_rating_and_title(self.__account.username, new_rating, new_title)
            self.__account.update_singleplayer_rating()
            self.__account.update_singleplayer_title()
    
    def __curr_milestone_rank(self, milestone): # Method to get current milestone rank (1 to 7) of any milestone collection
        for rank, comps in reversed(GameMilestones.MILESTONES.items()):
            if milestone >= comps:
                return rank
        else:
            return 0
    
    def update_milestone(self, data): # Method to update milestone after each game

        mode, board_size, difficulty, won = data

        if won:

            milestone = database.milestone(self.__account.username, bs := f"milestone_{board_size}x{board_size}")
            new_milestone = milestone + GameMilestones.MILESTONE_GAIN[difficulty] * (2 if mode == "Killer" else 1)
            database.set_milestone(self.__account.username, bs, new_milestone)

            old_rank = self.__curr_milestone_rank(milestone)
            new_rank = self.__curr_milestone_rank(new_milestone)

            if new_rank != old_rank:
                claimed = database.milestone_claimed(self.__account.username)
                idx = GameMilestones.BOARD_SIZE_IDXS[board_size] * 7 + new_rank - 1
                database.set_milestone_claimed(self.__account.username, claimed[:idx] + "1" + claimed[idx+1:])

            print(f"Milestone successfully updated for {self.__account.username}")
    
    def claim_reward(self, data): # Method to claim reward for a milestone (from game milestone screen)
        
        board_size, milestone_num = data
        claimed = database.milestone_claimed(self.__account.username)
        idx = GameMilestones.BOARD_SIZE_IDXS[board_size] * 7 + milestone_num - 1
        database.set_milestone_claimed(self.__account.username, claimed[:idx] + "0" + claimed[idx+1:])
        reward = GameMilestones.REWARDS[f"{board_size}x{board_size}"][milestone_num]
        if reward is not None and reward[0] == "H":
            bonus_hints = database.bonus_hints(self.__account.username)
            database.set_bonus_hints(self.__account.username, bonus_hints + reward[1])
        
        print(f"Milestone reward claimed")
        