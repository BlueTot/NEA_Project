import sqlite3
import os
import hashlib
import datetime

class DBError(Exception):
    pass

def __db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "accounts.db")

def __conn():
    return sqlite3.connect(__db_path())

def __update_db(sql):
    connection = __conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

def __fetch_data(sql):
    connection = __conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return data

def __setup():
    if not os.path.exists(__db_path()):
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
                    );""")
    
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
                    );""")

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
        );""")

def encrypt_password(password):
    salt = "sudoku"
    hashed = hashlib.md5((password+salt).encode())
    return hashed.hexdigest()

def next_preset_id():
    if (id := __fetch_data("""SELECT MAX(preset_id) FROM AppearancePresets;""")[0][0]) is not None:
        return id + 1
    else:
        return 0

def next_preset_number(username):
    if (num := __fetch_data(f"""SELECT MAX(preset_number) FROM AppearancePresets WHERE username='{username}';""")[0][0]) is not None:
        return num + 1
    else:
        return 1

def create_new_account(username, password):
    __setup()
    if password_at(username):
        raise DBError("Username already taken")
    __update_db(f"""INSERT INTO Accounts VALUES('{username}', 0, 'New Player', '{encrypt_password(password)}', 1, 0, 0, 0, 0, 0, '{'0'*35}', 0);""")
    __update_db(f"""INSERT INTO AppearancePresets VALUES({next_preset_id()}, '{username}', 1, '#f0f0f0', '#ffffff', '#aee8f5', 
                '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3');""")
    print(f"Account {username} created")

def delete_account(username):
    __setup()
    if password_at(username):
        __update_db(f"""DELETE FROM Accounts WHERE username='{username}';""")
        __update_db(f"""DELETE FROM AppearancePresets WHERE username='{username}';""")
        __update_db(f"""DELETE FROM Games WHERE username='{username}';""")
        print(f"Account {username} deleted")
    else:
        raise DBError("Username does not exist")

def password_at(username):
    __setup()
    return __fetch_data(f"""SELECT password FROM Accounts WHERE username = '{username}';""")

def appearance_config_at(username):
    __setup()
    return __fetch_data(f"""SELECT background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets INNER JOIN Accounts ON AppearancePresets.username = Accounts.username 
                        WHERE AppearancePresets.username = '{username}' AND AppearancePresets.preset_number = Accounts.current_appearance_preset_number;""")

def get_all_presets(username):
    __setup()
    return __fetch_data(f"""SELECT preset_number, background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets WHERE username='{username}';""")

def get_preset(username, preset_num):
    __setup()
    return __fetch_data(f"""SELECT background_colour, colour1, colour2, colour3, colour4, title_font, 
                        regular_font, killer_colour1, killer_colour2, killer_colour3, killer_colour4, killer_colour5 
                        FROM AppearancePresets WHERE username='{username}' AND preset_number={preset_num};""")[0]

def update_appearance_preset(username, preset_num, options):
    __setup()
    __update_db(f"""UPDATE AppearancePresets SET background_colour='{options[0]}', colour1='{options[1]}', colour2='{options[2]}',
                colour3='{options[3]}', colour4='{options[4]}', title_font='{options[5]}', regular_font='{options[6]}',
                 killer_colour1='{options[7]}', killer_colour2='{options[8]}', killer_colour3='{options[9]}', killer_colour4='{options[10]}',
                  killer_colour5='{options[11]}' WHERE username='{username}' AND preset_number={preset_num};""")
    print(f"Appearance Preset {preset_num} updated for {username}")

def create_new_appearance_preset(username, options):
    __setup()
    preset_num = next_preset_number(username)
    __update_db(f"""INSERT INTO AppearancePresets VALUES({next_preset_id()}, '{username}', {preset_num}, '{options[0]}', 
                '{options[1]}', '{options[2]}', '{options[3]}', '{options[4]}', '{options[5]}', '{options[6]}', '{options[7]}', 
                '{options[8]}', '{options[9]}', '{options[10]}', '{options[11]}');""")
    print(f"Appearance Preset {preset_num} created for for {username}")

def delete_appearance_preset(username, preset_num):
    __setup()
    __update_db(f"""DELETE FROM AppearancePresets WHERE username='{username}' AND preset_number={preset_num};""")

def get_current_appearance_preset_num(username):
    __setup()
    return __fetch_data(f"""SELECT current_appearance_preset_number FROM Accounts WHERE username='{username}';""")[0][0]

def set_current_appearance_preset(username, preset_num):
    __setup()
    __update_db(f"""UPDATE Accounts SET current_appearance_preset_number={preset_num} WHERE username='{username}';""")

def add_game(username, stats):
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

def change_username(orig_username, new_username):
    try:
        __setup()
        __update_db(f"""UPDATE Accounts SET username='{new_username}' WHERE username='{orig_username}';""")
        __update_db(f"""UPDATE Games SET username='{new_username}' WHERE username='{orig_username}';""")
        print(f"Username {orig_username} changed to {new_username}")
    except sqlite3.IntegrityError:
        raise DBError("Username already taken")

def change_password(username, new_password):
    __setup()
    __update_db(f"""UPDATE Accounts SET password='{encrypt_password(new_password)}' WHERE username='{username}';""")
    print(f"Password updated for username {username}")

def rating(username):
    return __fetch_data(f"""SELECT rating FROM Accounts WHERE username='{username}';""")

def title(username):
    return __fetch_data(f"""SELECT title FROM Accounts WHERE username='{username}';""")

def update_rating_and_title(username, rating, title):
    __setup()
    __update_db(f"""UPDATE Accounts SET rating={rating} WHERE username='{username}';""")
    __update_db(f"""UPDATE Accounts SET title='{title}' WHERE username='{username}';""")
    print(f"Rating and title updated for {username}")

def get_games_of(username):
    __setup()
    return __fetch_data(f"""SELECT * FROM Games WHERE username='{username}';""")

def num_of_games(username):
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}';""")[0][0]

def num_completed_games(username):
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' AND completed='True';""")[0][0]

def times_played(username, mode, board_size, difficulty):
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}';""")[0][0]

def num_completions(username, mode, board_size, difficulty):
    __setup()
    return __fetch_data(f"""SELECT COUNT(*) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True';""")[0][0]

def best_time(username, mode, board_size, difficulty):
    __setup()
    secs = __fetch_data(f"""SELECT MIN(time_to_complete) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True';""")[0][0]
    return str(datetime.timedelta(seconds=secs)) if secs is not None else "None"

def best_hardcore_time(username, mode, board_size, difficulty):
    __setup()
    secs = __fetch_data(f"""SELECT MIN(time_to_complete) FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True' AND hardcore='True';""")[0][0]
    return str(datetime.timedelta(seconds=secs)) if secs is not None else "None"

def milestone(username, board_size):
    __setup()
    return __fetch_data(f"""SELECT {board_size} FROM Accounts WHERE username='{username}';""")[0][0]

def milestone_claimed(username):
    __setup()
    return __fetch_data(f"""SELECT claimed FROM Accounts WHERE username='{username}';""")[0][0]

def set_milestone(username, board_size, new_milestone):
    __setup()
    __update_db(f"""UPDATE Accounts SET {board_size}={new_milestone} WHERE username='{username}';""")

def set_milestone_claimed(username, claimed):
    __setup()
    __update_db(f"""UPDATE Accounts SET claimed='{claimed}' WHERE username='{username}';""")

def bonus_hints(username):
    __setup()
    return __fetch_data(f"""SELECT bonus_hints FROM Accounts WHERE username='{username}';""")[0][0]

def set_bonus_hints(username, num_hints):
    __setup()
    __update_db(f"""UPDATE Accounts SET bonus_hints={num_hints} WHERE username='{username}';""")

def all_account_rating_data():
    __setup()
    return __fetch_data("""SELECT username, rating, title FROM Accounts""")

def leaderboard_best_time_data(mode, board_size, difficulty):
    return __fetch_data(f"""SELECT Accounts.username, Accounts.rating, Accounts.title, 
                        (SELECT MIN(Games.time_to_complete) FROM Games WHERE mode='{mode}' AND board_size={board_size}
                       AND difficulty='{difficulty}' AND completed='True' AND hardcore='True' AND Games.username=Accounts.username) 
                       FROM Accounts WHERE EXISTS (SELECT Games.time_to_complete FROM Games WHERE mode='{mode}' AND difficulty='{difficulty}'
                       AND completed='True' AND hardcore='True' AND Games.username=Accounts.username);""")

def leaderboard_milestone_data(board_size):
    return __fetch_data(f"""SELECT username, rating, title, milestone_{board_size} FROM Accounts;""")

if __name__ in "__main__":
    __setup()
    print(__fetch_data("""SELECT * FROM Accounts"""))
    print(__fetch_data(f"""SELECT username FROM Accounts"""))
    print(leaderboard_best_time_data("Normal", 4, "Easy"))

##C5B4E3