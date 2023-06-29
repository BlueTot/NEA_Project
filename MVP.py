def get_input(inp_string, choices):
    while True:
        choice = input(inp_string)
        if choice in choices:
            return choice
        else:
            print("Not one of the options ... try again!")

class UI:
    def __init__(self):
        pass

class Terminal(UI):
    def __init__(self):
        super().__init__()

class SudokuGame:
    def __init__(self):
        self.__terminal = Terminal()

    def play(self):
        mode_choice = get_input("Press (T) to play game in terminal mode, (Q) to quit the game", ["T", "Q"])
        if mode_choice == "T":
            self.__play_terminal()
        elif mode_choice == "Q":
            print("Game Successfully Closed")

    def __play_terminal(self):
        while True:
            main_menu_choice = get_input("Press (P) to play game, (Q) to quit", ["P", "Q"])
            if main_menu_choice == "P":
                self.__play_new_game()
            elif main_menu_choice == "Q":
                print("Game Successfully Closed")
                return

            

    def __play_new_game(self):
        pass
            










if __name__ in "__main__":
    game = SudokuGame()
    game.play()
