from sys import argv # Import object to get list of arguments entered in the terminal
from terminal import Terminal # Import Terminal class
from gui import GUI # Import GUI class

def print_usage(): # Print how to run the game in terminal
    print("""Welcome to Sudoku
          
    To start the program in terminal: 
          ENTER [python] sudoku.py t
    To start the program in GUI: 
          ENTER [python] sudoku.py g""")

def main():

    if len(argv) != 2: # If number of arguments is not 2
        print_usage()
        return

    if argv[1] == "t": # Run terminal if 't' option used
        game = Terminal()
    elif argv[1] == "g": # Run GUI if 'g' optin used
        game = GUI()
    else: # Otherwise print program usage
        print_usage()
        return
    
    game.run() # Start the game

if __name__ in "__main__": # Driver code
    main()
