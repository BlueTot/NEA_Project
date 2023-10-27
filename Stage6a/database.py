import sqlite3
import os
import hashlib

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
        __update_db("""CREATE TABLE Games(
                    game_id INTEGER PRIMARY KEY,
                    username VARCHAR(100),
                    mode VARCHAR(20),
                    difficulty VARCHAR(20),
                    board_size INTEGER,
                    orig_num_hints INTEGER,
                    rem_num_hints INTEGER,
                    timed BOOLEAN,
                    completed BOOLEAN,
                    time_to_complete FLOAT(24),
                    creation_date DATE,
                    creation_time TIME

        );""")

def encrypt_password(password):
    salt = "sudoku"
    hashed = hashlib.md5((password+salt).encode())
    return hashed.hexdigest()

def create_new_account(username, password):
    __setup()
    if password_at(username):
        raise DBError("Username already taken")
    __update_db(f"""INSERT INTO Passwords VALUES('{username}', '{encrypt_password(password)}');""")
    __update_db(f"""INSERT INTO AppearanceConfig VALUES('{username}', '#f0f0f0', '#ffffff', '#aee8f5',
                '#969696', '#ffcccb', 'LIBRARY 3 AM soft', 'Metropolis', '#ff7276', '#ffffe0', '#add8e6', '#90ee90', '#c5b4e3');""")
    print(f"Account {username} created")

def delete_account(username):
    __setup()
    if password_at(username):
        __update_db(f"""DELETE FROM Passwords WHERE username='{username}';""")
        __update_db(f"""DELETE FROM AppearanceConfig WHERE username='{username}';""")
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
                    '{stats[0]}', '{stats[1]}', {stats[2]}, {stats[3]}, {stats[4]},
                    '{stats[5]}', '{stats[6]}', {stats[7]}, '{stats[8]}', '{stats[9]}'
                );""")
    print(f"Game stats successfully saved to {username}")

if __name__ in "__main__":
    #create_new_account("admin", "admin")
    print(password_at("admin"))
    print(appearance_config_at("admin"))

    print(__fetch_data("""SELECT MAX(game_id) FROM Games""")[0][0])

    for line in __fetch_data("""SELECT * FROM Games"""):
        print(line)

##C5B4E3