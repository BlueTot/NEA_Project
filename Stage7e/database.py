import sqlite3 # Import sql database library
import os # Import os library
import hashlib # Import password hashing library
import datetime # Import datetime library

class DBError(Exception): #] Database Error
    pass

def __db_path(): # Function to get path of database file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "accounts.db")

def __conn(): # Connection to make changes to database
    return sqlite3.connect(__db_path())

def __update_db(sql): # Function to update database by excecuting given SQL
    connection = __conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

def __fetch_data(sql): # Function to fetch data from given SQL query
    connection = __conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return data

def __setup(): # Setup function to initialise database tables
    if not os.path.exists(__db_path()): # Check if database file already exists
        print("DB Setup")
        __update_db("""CREATE TABLE Accounts(
                    username VARCHAR(100) PRIMARY KEY,
                    rating INTEGER,
                    title VARCHAR(20),
                    password VARCHAR(200),
                    current_appearance_preset_number INTEGER,
                    milestone_4x4 INTEGER,
                    milestone_6x6 INTEGER,
                    milestone_9x9 INTEGER,
                    milestone_12x12 INTEGER,
                    milestone_16x16 INTEGER,
                    claimed VARCHAR(35),
                    bonus_hints INTEGER
                    );""") # Create Accounts Table to store account related data
    
        __update_db("""CREATE TABLE AppearancePresets(
                    preset_id INTEGER PRIMARY KEY,
                    username VARCHAR(100),
                    preset_number INTEGER,
                    background_colour VARCHAR(7),
                    colour1 VARCHAR(7),
                    colour2 VARCHAR(7),
                    colour3 VARCHAR(7),
                    colour4 VARCHAR(7),
                    title_font VARCHAR(100),
                    regular_font VARCHAR(100),
                    killer_colour1 VARCHAR(7),
                    killer_colour2 VARCHAR(7),
                    killer_colour3 VARCHAR(7),
                    killer_colour4 VARCHAR(7),
                    killer_colour5 VARCHAR(7)
                    );""") # Create AppearancePresets Table to store user's appearance presets (one account has multiple appearance presets)

        __update_db("""CREATE TABLE Games(
                    game_id INTEGER PRIMARY KEY,
                    username VARCHAR(100),
                    mode VARCHAR(20),
                    difficulty VARCHAR(20),
                    board_size INTEGER,
                    orig_num_auto_notes INTEGER,
                    rem_num_auto_notes INTEGER,
                    orig_num_hints INTEGER,
                    rem_num_hints INTEGER,
                    timed BOOLEAN,
                    completed BOOLEAN,
                    hardcore BOOLEAN,
                    time_to_complete FLOAT(24),
                    creation_date DATE,
                    creation_time TIME
        );""") # Create Games Table to store resigned / won games (one account has multiple games)

def encrypt_password(password): # Function to hash password
    salt = "sudoku"
    hashed = hashlib.md5((password+salt).encode())
    return hashed.hexdigest()

def next_preset_id(): # Get next appearance preset ID (global)
    if (id := __fetch_data("""SELECT MAX(preset_id) FROM AppearancePresets;""")[0][0]) is not None:
        return id + 1
    else:
        return 0

def next_preset_number(username): # Get next appearance preset number (local, relative to user)
    if (num := __fetch_data(f"""SELECT MAX(preset_number) FROM AppearancePresets WHERE username='{username}';""")[0][0]) is not None:
        return num + 1
    else:
        return 1

def create_new_account(username, password): # Query to create new account when given username and pasword
    __setup()
    if password_at(username):
        raise DBError("Username already taken")
    __update_db(f"""INSERT INTO Accounts VALUES('{username}', 0, 'New Player', '{encrypt_password(password)}', 1, 0, 0, 0, 0, 0, '{'0'*35}', 0);""")
    __update_db(f"""INSERT INTO AppearancePresets VALUES({next_preset_id()}, '{username}', 1, '#f0f0f0', '#ffffff', '#aee8f5', 
                '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3');""")
    print(f"Account {username} created")

def delete_account(username): # Query to delete account
    __setup()
    if password_at(username):
        __update_db(f"""DELETE FROM Accounts WHERE username='{username}';""")
        __update_db(f"""DELETE FROM AppearancePresets WHERE username='{username}';""")
        __update_db(f"""DELETE FROM Games WHERE username='{username}';""")
        print(f"Account {username} deleted")
    else:
        raise DBError("Username does not exist")

def password_at(username): # Query to get password of a given username, used to check against password inputted when signing in
    __setup()
    return __fetch_data(f"""SELECT password FROM Accounts WHERE username = '{username}';""")

def appearance_config_at(username): # Query to get current appearance preset of a given username / account
    __setup()
    return __fetch_data(f"""SELECT background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets INNER JOIN Accounts ON AppearancePresets.username = Accounts.username 
                        WHERE AppearancePresets.username = '{username}' AND AppearancePresets.preset_number = Accounts.current_appearance_preset_number;""")

def get_all_presets(username): # Query to get all appearance presets of a given account, used in ViewGUIPresetsScreen to display all stored presets to the user
    __setup()
    return __fetch_data(f"""SELECT preset_number, background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets WHERE username='{username}';""")

def get_preset(username, preset_num): # Query to get appearance preset of a given preset number for a given account, used to display settings when user browses stored presets
    __setup()
    return __fetch_data(f"""SELECT background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets WHERE username='{username}' AND preset_number={preset_num};""")[0]

def update_appearance_preset(username, preset_num, options): # Query to edit existing appearance preset, used when user edits a preset and saves it
    __setup()
    __update_db(f"""UPDATE AppearancePresets SET background_colour='{options[0]}', colour1='{options[1]}', colour2='{options[2]}',
                colour3='{options[3]}', colour4='{options[4]}', title_font='{options[5]}', regular_font='{options[6]}',
                 killer_colour1='{options[7]}', killer_colour2='{options[8]}', killer_colour3='{options[9]}', killer_colour4='{options[10]}',
                  killer_colour5='{options[11]}' WHERE username='{username}' AND preset_number={preset_num};""")
    print(f"Appearance Preset {preset_num} updated for {username}")

def create_new_appearance_preset(username, options): # Query to create new appearance preset, used when user saves a newly created preset
    __setup()
    preset_num = next_preset_number(username)
    __update_db(f"""INSERT INTO AppearancePresets VALUES({next_preset_id()}, '{username}', {preset_num}, '{options[0]}', 
                '{options[1]}', '{options[2]}', '{options[3]}', '{options[4]}', '{options[5]}', '{options[6]}', '{options[7]}', 
                '{options[8]}', '{options[9]}', '{options[10]}', '{options[11]}');""")
    print(f"Appearance Preset {preset_num} created for for {username}")

def delete_appearance_preset(username, preset_num): # Query to delete appearance preset
    __setup()
    __update_db(f"""DELETE FROM AppearancePresets WHERE username='{username}' AND preset_number={preset_num};""")

def get_current_appearance_preset_num(username): #Query to get preset number (local) of current appearance preset that is in use
    __setup()
    return __fetch_data(f"""SELECT current_appearance_preset_number FROM Accounts WHERE username='{username}';""")[0][0]

def set_current_appearance_preset(username, preset_num): # Query to set current appearance preset given preset number and username
    __setup()
    __update_db(f"""UPDATE Accounts SET current_appearance_preset_number={preset_num} WHERE username='{username}';""")

def add_game(username, stats): # Query to add game stats to Games table when a game is completed or resigned
    __setup()
    if (id := __fetch_data("""SELECT MAX(game_id) FROM Games;""")[0][0]) is not None:
        game_id = id + 1
    else:
        game_id = 0
    __update_db(f"""INSERT INTO Games VALUES('{game_id}', '{username}', 
                    '{stats[0]}', '{stats[1]}', {stats[2]}, {stats[3]}, {stats[4]}, {stats[5]}, {stats[6]},
                    '{stats[7]}', '{stats[8]}', '{stats[9]}', {stats[10]}, '{stats[11]}', '{stats[12]}'
                );""")
    print(f"Game stats successfully saved to {username}")

def change_username(orig_username, new_username): # Query to change username given original username and new username (ManageAccount screen)
    try:
        __setup()
        __update_db(f"""UPDATE Accounts SET username='{new_username}' WHERE username='{orig_username}';""")
        __update_db(f"""UPDATE AppearancePresets SET username='{new_username}' WHERE username='{orig_username}';""")
        __update_db(f"""UPDATE Games SET username='{new_username}' WHERE username='{orig_username}';""")
        print(f"Username {orig_username} changed to {new_username}")
    except sqlite3.IntegrityError:
        raise DBError("Username already taken")

def change_password(username, new_password): # Query to change password given username and new password (ManageAccount screen)
    __setup()
    __update_db(f"""UPDATE Accounts SET password='{encrypt_password(new_password)}' WHERE username='{username}';""")
    print(f"Password updated for username {username}")

def rating(username): # Query to get rating of username
    return __fetch_data(f"""SELECT rating FROM Accounts WHERE username='{username}';""")

def title(username): # Query to get title of username
    return __fetch_data(f"""SELECT title FROM Accounts WHERE username='{username}';""")

def update_rating_and_title(username, rating, title): # Query to update rating and title of username after each game
    __setup()
    __update_db(f"""UPDATE Accounts SET rating={rating} WHERE username='{username}';""")
    __update_db(f"""UPDATE Accounts SET title='{title}' WHERE username='{username}';""")
    print(f"Rating and title updated for {username}")

def get_games_of(username): # Query to get all games that belong to a given account
    __setup()
    return __fetch_data(f"""SELECT * FROM Games WHERE username='{username}';""")

def num_of_games(username): # Query to get the number of games played by a given account
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}';""")[0][0]

def num_completed_games(username): # Query to get the number of completed games of a given account
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' AND completed='True';""")[0][0]

def times_played(username, mode, board_size, difficulty): # Query to get the number of times a user played a certain gamemode
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}';""")[0][0]

def num_completions(username, mode, board_size, difficulty): # Query to get the number of times a user completed a board of a certain gamemode
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True';""")[0][0]

def best_time(username, mode, board_size, difficulty): # Query to get the user's best time in a certain gamemode
    __setup()
    secs = __fetch_data(f"""SELECT MIN(time_to_complete) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True';""")[0][0]
    return str(datetime.timedelta(seconds=secs)) if secs is not None else "None"

def best_hardcore_time(username, mode, board_size, difficulty): # Query to get the user's best hardcore (no hints) time in a certain gamemode
    __setup()
    secs = __fetch_data(f"""SELECT MIN(time_to_complete) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True' AND hardcore='True';""")[0][0]
    return str(datetime.timedelta(seconds=secs)) if secs is not None else "None"

def milestone(username, board_size): # Query to get the milestone number of an account given the username and board size
    __setup()
    return __fetch_data(f"""SELECT {board_size} FROM Accounts WHERE username='{username}';""")[0][0]

def milestone_claimed(username): # Query to get the claimed string of a given account that encodes whether the user has claimed a reward for each milestone
    __setup()
    return __fetch_data(f"""SELECT claimed FROM Accounts WHERE username='{username}';""")[0][0]

def set_milestone(username, board_size, new_milestone): # Query to set the milestone number of a given board size
    __setup()
    __update_db(f"""UPDATE Accounts SET {board_size}={new_milestone} WHERE username='{username}';""")

def set_milestone_claimed(username, claimed): # Query to set the claimed string of a given account after user claims a reward or unlocks a new milestone
    __setup()
    __update_db(f"""UPDATE Accounts SET claimed='{claimed}' WHERE username='{username}';""")

def bonus_hints(username): # Query to get the number of bonus hints an account currently has
    __setup()
    return __fetch_data(f"""SELECT bonus_hints FROM Accounts WHERE username='{username}';""")[0][0]

def set_bonus_hints(username, num_hints): # Query to update the numnber of bonus hints an account currently has after claiming rewards
    __setup()
    __update_db(f"""UPDATE Accounts SET bonus_hints={num_hints} WHERE username='{username}';""")

def all_account_rating_data(): # Query to get the username, rating and title of all registered accounts (used in leaderboard)
    __setup()
    return __fetch_data("""SELECT username, rating, title FROM Accounts""")

def leaderboard_best_time_data(mode, board_size, difficulty): # Query to get the username, rating, title and best time in a certain gamemode of all registered accounts (used in leaderboard)
    return __fetch_data(f"""SELECT Accounts.username, Accounts.rating, Accounts.title, 
                        (SELECT MIN(Games.time_to_complete) FROM Games WHERE mode='{mode}' AND board_size={board_size}
                       AND difficulty='{difficulty}' AND completed='True' AND hardcore='True' AND Games.username=Accounts.username) 
                       FROM Accounts WHERE EXISTS (SELECT Games.time_to_complete FROM Games WHERE mode='{mode}' AND difficulty='{difficulty}'
                       AND completed='True' AND hardcore='True' AND Games.username=Accounts.username);""")

def leaderboard_milestone_data(board_size): # Query to get the username, rating, title and milestone number of all registered accounts (used in leaderboard)
    return __fetch_data(f"""SELECT username, rating, title, milestone_{board_size} FROM Accounts;""")

# if __name__ in "__main__":
#     __setup()
#     print(__fetch_data("""SELECT * FROM Accounts"""))
#     print(__fetch_data(f"""SELECT username FROM Accounts"""))
#     print(leaderboard_best_time_data("Normal", 4, "Easy"))
#     print(__fetch_data("""SELECT * FROM AppearancePresets"""))
#     print(appearance_config_at("bluetot"))

##C5B4E3