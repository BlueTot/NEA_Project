from board import BoardGenerator
import json

class GameGenerator:

    MODES = ("Normal", "Killer")
    BOARD_SIZES = (4, 6, 9, 12, 16)
    DIFFICULTIES = ("Easy", "Medium", "Hard", "Challenge")
    DEFAULT_DIRECTORY = "game_bank"

    def __init__(self):
        pass
    
    def generate(self):
        for mode in self.MODES:
            for board_size in self.BOARD_SIZES:
                for difficulty in self.DIFFICULTIES:
                    print(mode, board_size, difficulty)
                    if board_size == 16 and difficulty in ("Hard", "Challenge"):
                        continue
                    self.__create_boards(mode, difficulty, board_size)
    
    def __create_boards(self, mode, difficulty, board_size):
        with open(f"{self.DEFAULT_DIRECTORY}/{mode}{board_size}{difficulty}.json", "w") as f:
            boards = {}
            for id in range(100):
                board = BoardGenerator.new_board(mode, difficulty, board_size)
                boards[id] = board.hash()
            f.write(json.dumps(boards, indent=4))

if __name__ in "__main__":
    game_generator = GameGenerator()
    game_generator.generate()

                    
