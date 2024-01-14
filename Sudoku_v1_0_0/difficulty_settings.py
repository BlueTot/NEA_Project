from math import exp # import e^x exponential function

NORMAL_NUM_GIVENS = {9: {"Easy": 43, "Medium": 35, "Hard": 29, "Expert": 25}} # num givens for 9x9
KILLER_NUM_GIVENS = {9: {"Easy": 32, "Medium": 22, "Hard": 14, "Expert": 8}} # num givens for 9x9 killer
DIFFICULTY_NUMS = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3} # Number associated with each difficulty for calculation purposes
GROWTH_FACTORS = {"Normal": {4: 0.85, 6: 0.85, 12: 0.1, 16: 0.025}, # Growth factors to calculate the number of given numbers for each board size and mode
                "Killer": {4: 0.7, 6: 0.7, 12:0.1, 16: 0.025}}

'''Scaling function, uses exponential function Ae^(-Bx) + C 
where A,B,C are constants and B is a scalable constant based on GROWTH_FACTORS, x is the difficulty number'''
def __num_givens(mode, board_size, difficulty): # Function to calculate the number of givens for a given gamemode
    if mode == "Normal":
        B, C = 0.35 * GROWTH_FACTORS[mode][board_size], 16
        A = NORMAL_NUM_GIVENS[9][difficulty] - C
    else:
        A, B, C = KILLER_NUM_GIVENS[9][difficulty], 0.45 * GROWTH_FACTORS[mode][board_size], 0
    givens = A*exp(-B*DIFFICULTY_NUMS[difficulty])+C # use exponential function to calculate number of given numbers
    return int(givens / (9**2) * (board_size**2)) # scale by number of squares on the board

def get_num_givens(): # Get num givens for normal and killer modes

    NUM_GIVENS = {}

    for board_size in [4, 6, 12, 16]: # scale to 4x4, 6x6, 12x12, 16x16
        NORMAL_NUM_GIVENS[board_size] = {diff : __num_givens("Normal", board_size, diff) for diff in ("Easy", "Medium", "Hard", "Expert")}

    for board_size in [4, 6, 12, 16]: # scale to 4x4, 6x6, 12x12, 16x16 killer
        KILLER_NUM_GIVENS[board_size] = {diff : __num_givens("Killer", board_size, diff) for diff in ("Easy", "Medium", "Hard", "Expert")}
    
    NUM_GIVENS["Normal"] = NORMAL_NUM_GIVENS
    NUM_GIVENS["Killer"] = KILLER_NUM_GIVENS

    return NUM_GIVENS
