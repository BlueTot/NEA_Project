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

def encrypt_password(password):
    salt = "sudoku"
    hashed = hashlib.md5((password+salt).encode())
    return hashed.hexdigest()

def create_new_account(username, password):
    __setup()
    if password_at(username):
        raise DBError("Username already taken")
    __update_db(f"""INSERT INTO Passwords VALUES('{username}', '{encrypt_password(password)}');""")
    print(f"Account {username} created")

def delete_account(username):
    __setup()
    if password_at(username):
        __update_db(f"""DELETE FROM Passwords WHERE username='{username}';""")
        print(f"Account {username} deleted")
    else:
        raise DBError("Username does not exist")

def password_at(username):
    __setup()
    return __fetch_data(f"""SELECT Passwords.password FROM Passwords WHERE Passwords.username = '{username}';""")

if __name__ in "__main__":
    create_new_account("bluetot", "abc")
    print(password_at("bluetot"))
    delete_account("bluetot")
    print(password_at("bluetot"))
