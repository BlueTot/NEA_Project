from math import exp

NORMAL_NUM_GIVENS = {9: {"Easy": 43, "Medium": 35, "Hard": 29, "Expert": 25}} # num givens for 9x9
KILLER_NUM_GIVENS = {9: {"Easy": 32, "Medium": 22, "Hard": 14, "Expert": 8}} # num givens for 9x9 killer
DIFFICULTY_NUMS = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3}
GROWTH_FACTORS = {"Normal": {4: 0.85, 6: 0.85, 12: 0.1, 16: 0.025},
                "Killer": {4: 0.7, 6: 0.7, 12:0.1, 16: 0.025}}

'''Scaling function, uses exponential function Ae^(-Bx) + C 
where A,B,C are constants and B is a scalable constant based on GROWTH_FACTORS, x is the difficulty number'''
def __num_givens(mode, board_size, difficulty): 
    if mode == "Normal":
        B, C = 0.35 * GROWTH_FACTORS[mode][board_size], 16
        A = NORMAL_NUM_GIVENS[9][difficulty] - C
    else:
        A, B, C = KILLER_NUM_GIVENS[9][difficulty], 0.45 * GROWTH_FACTORS[mode][board_size], 0
    givens = A*exp(-B*DIFFICULTY_NUMS[difficulty])+C
    return int(givens / (9**2) * (board_size**2))

def get_num_givens(): # Get num givens for normal and killer modes

    for board_size in [4, 6, 12, 16]: # scale to 4x4, 6x6, 12x12, 16x16
        NORMAL_NUM_GIVENS[board_size] = {diff : __num_givens("Normal", board_size, diff) for diff in ("Easy", "Medium", "Hard", "Expert")}

    for board_size in [4, 6, 12, 16]: # scale to 4x4, 6x6, 12x12, 16x16 killer
        KILLER_NUM_GIVENS[board_size] = {diff : __num_givens("Killer", board_size, diff) for diff in ("Easy", "Medium", "Hard", "Expert")}

    return NORMAL_NUM_GIVENS, KILLER_NUM_GIVENS

if __name__ in "__main__":
    for d in get_num_givens():
        for k, v in d.items():
            print(k, v)
        print()

'''OUTPUT OF FUNCTION SHOULD GIVE:

9 {'Easy': 43, 'Medium': 35, 'Hard': 29, 'Expert': 25}
4 {'Easy': 8, 'Medium': 5, 'Hard': 4, 'Expert': 3}
6 {'Easy': 19, 'Medium': 13, 'Hard': 10, 'Expert': 8}
12 {'Easy': 76, 'Medium': 61, 'Hard': 49, 'Expert': 42}
16 {'Easy': 135, 'Medium': 110, 'Hard': 90, 'Expert': 78}

9 {'Easy': 32, 'Medium': 22, 'Hard': 14, 'Expert': 8}
4 {'Easy': 6, 'Medium': 3, 'Hard': 1, 'Expert': 0}
6 {'Easy': 14, 'Medium': 7, 'Hard': 3, 'Expert': 1}
12 {'Easy': 56, 'Medium': 37, 'Hard': 22, 'Expert': 12}
16 {'Easy': 101, 'Medium': 68, 'Hard': 43, 'Expert': 24}

'''
