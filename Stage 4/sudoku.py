from sys import argv
from terminal import Terminal
from gui import GUI

def print_usage(): # print how to run the game
    print("""Welcome to Sudoku
          
    To start the program in terminal: 
          ENTER [python] sudoku.py t
    To start the program in GUI: 
          ENTER [python] sudoku.py g""")

def main():

    if len(argv) != 2:
        print_usage()
        return

    if argv[1] == "t": # terminal
        game = Terminal()
    elif argv[1] == "g": # gui
        game = GUI()
    else:
        print_usage()
        return
    
    game.run() # start game

if __name__ in "__main__": # driver code
    main()
