from sys import argv
from ui import Terminal, GUI

def print_usage():
    print("""Welcome to Sudoku
          
    To start the program in terminal: 
          ENTER [python] sudoku.py t
    To start the program in GUI: 
          ENTER [python] sudoku.py g""")

def main():

    if len(argv) != 2:
        print_usage()
        return

    if argv[1] == "t":
        game = Terminal()
        game.run()
    elif argv[1] == "g":
        game = GUI()
        game.run()
    else:
        print_usage()

if __name__ in "__main__":
    main()
