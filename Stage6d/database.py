import sqlite3
import os
import hashlib
import datetime

# def time_format(secs):
#     if secs is None:
#         return None
#     return f"{int(secs // 3600)}h {(int(secs // 60)) % 60}m {int(secs % 60)}s"

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
        __update_db("""CREATE TABLE Passwords(
        username VARCHAR(100) PRIMARY KEY,
        password VARCHAR(200)
        );""")
        __update_db("""CREATE TABLE Ratings(
                    username VARCHAR(100) PRIMARY KEY,
                    singleplayer_rating INTEGER,
                    singleplayer_title VARCHAR(20)
        );""")
        __update_db("""CREATE TABLE AppearanceConfig(
                    username VARCHAR(100) PRIMARY KEY,
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
        __update_db("""CREATE TABLE GameMilestones(
                    username VARCHAR(100) PRIMARY KEY,
                    milestone_4x4 INTEGER,
                    milestone_6x6 INTEGER,
                    milestone_9x9 INTEGER,
                    milestone_12x12 INTEGER,
                    milestone_16x16 INTEGER,
                    claimed VARCHAR(35)
        )""")
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
        __update_db("""CREATE TABLE MilestoneRewards(
                    username VARCHAR(100) PRIMARY KEY,
                    bonus_hints INTEGER
        )""")

def encrypt_password(password):
    salt = "sudoku"
    hashed = hashlib.md5((password+salt).encode())
    return hashed.hexdigest()

def create_new_account(username, password):
    __setup()
    if password_at(username):
        raise DBError("Username already taken")
    __update_db(f"""INSERT INTO Passwords VALUES('{username}', '{encrypt_password(password)}');""")
    __update_db(f"""INSERT INTO Ratings VALUES('{username}', 0, 'New Player');""")
    __update_db(f"""INSERT INTO GameMilestones VALUES('{username}', 0, 0, 0, 0, 0, '{'0'*35}');""")
    __update_db(f"""INSERT INTO MilestoneRewards VALUES('{username}', 0);""")
    __update_db(f"""INSERT INTO AppearanceConfig VALUES('{username}', '#f0f0f0', '#ffffff', '#aee8f5',
                '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3');""")
    print(f"Account {username} created")

def delete_account(username):
    __setup()
    if password_at(username):
        __update_db(f"""DELETE FROM Passwords WHERE username='{username}';""")
        __update_db(f"""DELETE FROM Ratings WHERE username='{username}';""")
        __update_db(f""""DELETE FROM GameMilestones WHERE username='{username}';""")
        __update_db(f"""DELETE FROM MilestoneRewards WHERE username='{username}';""")
        __update_db(f"""DELETE FROM AppearanceConfig WHERE username='{username}';""")
        __update_db(f"""DELETE FROM Games WHERE username='{username}';""")
        print(f"Account {username} deleted")
    else:
        raise DBError("Username does not exist")

def password_at(username):
    __setup()
    return __fetch_data(f"""SELECT Passwords.password FROM Passwords WHERE Passwords.username = '{username}';""")

def appearance_config_at(username):
    __setup()
    return __fetch_data(f"""SELECT * FROM AppearanceConfig WHERE AppearanceConfig.username = '{username}';""")

def update_appearance_config(username, options):
    __setup()
    __update_db(f"""DELETE FROM AppearanceConfig WHERE username='{username}';""")
    options_string = ",".join([f"'{option}'" for option in options])
    __update_db(f"""INSERT INTO AppearanceConfig VALUES('{username}', {options_string});""")
    print(f"Appearance Config updated for {username}")

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
    __setup()
    __update_db(f"""UPDATE Passwords SET username='{new_username}' WHERE username='{orig_username}';""")
    __update_db(f"""UPDATE Ratings SET username='{new_username}' WHERE username='{orig_username}';""")
    __update_db(f"""UPDATE GameMilestones SET username='{new_username}' WHERE usernames='{orig_username}';""")
    __update_db(f"""UPDATE AppearanceConfig SET username='{new_username}' WHERE username='{orig_username}';""")
    __update_db(f"""UPDATE Games SET username='{new_username}' WHERE username='{orig_username}';""")
    print(f"Username {orig_username} changed to {new_username}")

def change_password(username, new_password):
    __setup()
    __update_db(f"""UPDATE Passwords SET password='{encrypt_password(new_password)}' WHERE username='{username}';""")
    print(f"Password updated for username {username}")

def singleplayer_rating(username):
    return __fetch_data(f"""SELECT singleplayer_rating FROM Ratings WHERE username='{username}';""")

def singleplayer_title(username):
    return __fetch_data(f"""SELECT singleplayer_title FROM Ratings WHERE username='{username}';""")

def update_singleplayer_rating_and_title(username, rating, title):
    __setup()
    __update_db(f"""UPDATE Ratings SET singleplayer_rating={rating} WHERE username='{username}';""")
    __update_db(f"""UPDATE Ratings SET singleplayer_title='{title}' WHERE username='{username}';""")
    print(f"Rating and title updated for {username}")

def get_games_of(username):
    __setup()
    return __fetch_data(f"""SELECT * FROM Games WHERE username='{username}';""")

def num_of_games(username):
    __setup()
    return len(get_games_of(username))

def num_completed_games(username):
    __setup()
    return len(__fetch_data(f"""SELECT * FROM Games WHERE username='{username}' AND completed='True';"""))

def times_played(username, mode, board_size, difficulty):
    __setup()
    return len(__fetch_data(f"""SELECT * FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}';"""))

def num_completions(username, mode, board_size, difficulty):
    __setup()
    return len(__fetch_data(f"""SELECT * FROM Games WHERE username='{username}' 
                            AND mode='{mode}' AND board_size={board_size} AND difficulty='{difficulty}'
                            AND completed='True';"""))

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
    return __fetch_data(f"""SELECT {board_size} FROM GameMilestones WHERE username='{username}';""")[0][0]

def milestone_claimed(username):
    __setup()
    return __fetch_data(f"""SELECT claimed FROM GameMilestones WHERE username='{username}';""")[0][0]

def set_milestone(username, board_size, new_milestone):
    __setup()
    __update_db(f"""UPDATE GameMilestones SET {board_size}={new_milestone} WHERE username='{username}';""")

def set_milestone_claimed(username, claimed):
    __setup()
    __update_db(f"""UPDATE GameMilestones SET claimed='{claimed}' WHERE username='{username}';""")

def bonus_hints(username):
    __setup()
    return __fetch_data(f"""SELECT bonus_hints FROM MilestoneRewards WHERE username='{username}';""")[0][0]

def set_bonus_hints(username, num_hints):
    __setup()
    __update_db(f"""UPDATE MilestoneRewards SET bonus_hints={num_hints} WHERE username='{username}';""")

def flip_list(lst):
    cols = len(lst[0])
    lst2 = [[] for _ in range(cols)]
    for col in range(cols):
        for row in lst:
            lst2[col].append(row[col])
    return lst2

def all_account_rating_data():
    __setup()
    return __fetch_data("""SELECT * FROM Ratings""")

def all_best_time_data(mode, board_size, difficulty):
    best_time_data = []
    for data in __fetch_data("""SELECT username from Ratings"""):
        username = data[0]
        best_time_data.append(best_hardcore_time(username, mode, board_size, difficulty))
    return best_time_data

def leaderboard_best_time_data(mode, board_size, difficulty):
    rating_data = [list(i) for i in all_account_rating_data()]
    best_time_data = all_best_time_data(mode, board_size, difficulty)
    for i in range(len(rating_data)):
        rating_data[i].append(best_time_data[i])
    return rating_data

def all_milestone_data(board_size):
    milestone_data = []
    for data in __fetch_data("""SELECT username from Ratings"""):
        username = data[0]
        milestone_data.append(milestone(username, f"milestone_{board_size}"))
    return milestone_data

def leaderboard_milestone_data(board_size):
    rating_data = [list(i) for i in all_account_rating_data()]
    best_time_data = all_milestone_data(board_size)
    for i in range(len(rating_data)):
        rating_data[i].append(best_time_data[i])
    return rating_data

if __name__ in "__main__":
    __setup()
    #create_new_account("admin", "admin")
    # print(password_at("admin"))
    # print(appearance_config_at("admin"))
    print(__fetch_data("""SELECT * FROM Passwords"""))

    print(__fetch_data("""SELECT * FROM Ratings"""))

    print(__fetch_data("""SELECT MAX(game_id) FROM Games""")[0][0])

    for line in __fetch_data("""SELECT * FROM Games"""):
        print(line) 
    
    print("\nadmin games")
    for game in get_games_of("admin"):
        print(game)
    
    print(best_time("admin", "Normal", 4, "Easy"))
    print(best_hardcore_time("admin", "Normal", 4, "Easy"))
    print(milestone("admin", "milestone_4x4"))
    print(milestone_claimed("admin"))
    print(bonus_hints("admin"))
    print(all_account_rating_data())
    print(__fetch_data("""SELECT * FROM GameMilestones"""))
    # set_milestone("admin", "milestone_4x4", 6)
    # set_milestone_claimed("admin", "0"*35)
    print(all_best_time_data("Normal", 4, "Expert"))
    print(best_hardcore_time("test2", "Normal", 4, "Expert"))

##C5B4E3