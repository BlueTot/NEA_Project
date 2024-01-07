import os
import shutil

PATH = "stage7e/"

def reset_database():
    if os.path.exists(path := PATH + "accounts.db"):
        os.remove(path)
    shutil.rmtree(gpath := PATH + "games")
    os.mkdir(gpath)

if __name__ in "__main__":
    reset_database()
    print("Reset Successful")