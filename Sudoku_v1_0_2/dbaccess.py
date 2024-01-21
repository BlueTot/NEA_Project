from database import __fetch_data
from database import *
from rating_calc import get_title

if __name__ in "__main__":
    print(__fetch_data("""SELECT * FROM Accounts"""))
    print(__fetch_data("""SELECT * FROM AppearancePresets"""))
    print(__fetch_data("""SELECT * FROM Games"""))
    update_rating_and_title("admin", 523, get_title(523))
    