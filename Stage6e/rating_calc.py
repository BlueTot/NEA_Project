from math import exp, e, log # Import e^x function, e constant and ln function

DIFFICULTY_NUMS = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3}

# Recommended ratings for each difficulty (16x16 Expert is omitted)
RECOMMENDED_RATINGS = {("Normal", 4, "Easy"): 0, ("Normal", 4, "Medium"): 40, ("Normal", 4, "Hard"): 80, ("Normal", 4, "Expert"): 120,
                       ("Normal", 6, "Easy"): 160, ("Normal", 6, "Medium"): 220, ("Normal", 6, "Hard"): 280, ("Normal", 6, "Expert"): 350,
                       ("Normal", 9, "Easy"): 400, ("Normal", 9, "Medium"): 600, ("Normal", 9, "Hard"): 800, ("Normal", 9, "Expert"): 1100,
                       ("Normal", 12, "Easy"): 1000, ("Normal", 12, "Medium"): 1200, ("Normal", 12, "Hard"): 1400, ("Normal", 12, "Expert"): 1600,
                       ("Normal", 16, "Easy"): 1200, ("Normal", 16, "Medium"): 1500, ("Normal", 16, "Hard"): 1800, ("Normal", 16, "Expert"): None,

                       ("Killer", 4, "Easy"): 10, ("Killer", 4, "Medium"): 50, ("Killer", 4, "Hard"): 90, ("Killer", 4, "Expert"): 130,
                       ("Killer", 6, "Easy"): 170, ("Killer", 6, "Medium"): 230, ("Killer", 6, "Hard"): 290, ("Killer", 6, "Expert"): 360,
                       ("Killer", 9, "Easy"): 410, ("Killer", 9, "Medium"): 630, ("Killer", 9, "Hard"): 850, ("Killer", 9, "Expert"): 1200,
                       ("Killer", 12, "Easy"): 1050, ("Killer", 12, "Medium"): 1350, ("Killer", 12, "Hard"): 1500, ("Killer", 12, "Expert"): 1650,
                       ("Killer", 16, "Easy"): 1500, ("Killer", 16, "Medium"): 1700, ("Killer", 16, "Hard"): 1950, ("Killer", 16, "Expert"): None
}

def average_time_to_complete(mode, board_size, difficulty):
    a = {4 : 25, 6: 45, 9: 240, 12: 450, 16: 770}[board_size]
    b = 0.775 + 0.30*{4: -2.5, 6: -1.5, 9: 0, 12: 0.05, 16: 0.1}[board_size]
    if mode == "Killer":
        b *= 1.5
    return round(a*exp(b*DIFFICULTY_NUMS[difficulty]))

def title(rating):
    if rating >= 2000:
        return "Master"
    elif rating >= 1600:
        return "Expert"
    elif rating >= 1200:
        return "Advanced"
    elif rating >= 800:
        return "Intermediate"
    elif rating >= 400:
        return "Beginner"
    else:
        return "New Player"

# Calculation Constants
ACTIVE_RANGE = 100 # b
XP_PER_RUN = 15 # k

'''RATING FORMULA: y = {a<x<a+b : k, x>a : round(ke^{-1/(10eb)*(x-a-b)^2),x<a:round(2k-ke^{-1/(10eb)*(x-a)^2)}'''
def __rating_gain(mode, board_size, difficulty, rating):
    recommended_rating = RECOMMENDED_RATINGS[(mode, board_size, difficulty)] # a
   
    if recommended_rating <= rating <= recommended_rating + ACTIVE_RANGE: # if a < x < a + b
        return XP_PER_RUN # k
    elif rating > recommended_rating: # if x > a
        return round(XP_PER_RUN * exp(-1/(10*e*ACTIVE_RANGE) * (rating - recommended_rating - ACTIVE_RANGE) ** 2)) # ke^(-1/(10eb) * (x-a-b)^2)
    elif rating < recommended_rating:
        return round(2*XP_PER_RUN - XP_PER_RUN*exp(-1/(10*e*ACTIVE_RANGE) * (rating - recommended_rating) ** 2)) # 2k - ke^(-1/(10eb) * (x-a)^2)

# Exponential scaling formula for rating gain using time and base rating gain calculated from rating
def __rating_gain_with_time(mode, board_size, difficulty, rating, time):
    base_rating = __rating_gain(mode, board_size, difficulty, rating) # R
    t_avg = average_time_to_complete(mode, board_size, difficulty) # T
    return round(5*base_rating/3 * exp(-log(2.5)/t_avg * time) + base_rating / 3) # 5R/3 * e^(-ln(2.5)/T * t) + R/3

# Linearly scaling formula for rating gain given number of auto notes used and number of hints used
def rating_gain(mode, board_size, difficulty, rating, time, num_auto_notes_used, orig_num_auto_notes, num_hints_used, orig_num_hints):
    base_rating = __rating_gain_with_time(mode, board_size, difficulty, rating, time)
    try:
        factor = 1 - ((num_auto_notes_used + num_hints_used * (board_size ** 0.5)) / (orig_num_auto_notes + orig_num_hints * (board_size ** 0.5))) # 1 - (n + sqrt(s)*h) / (N + sqrt(s)*H)
    except ZeroDivisionError:
        factor = 1
    return round(base_rating * factor)

'''RATING FORMULA: y = 2k - rating_gain(...)'''
def rating_loss(mode, board_size, difficulty, rating):
    return 2*XP_PER_RUN - __rating_gain(mode, board_size, difficulty, rating) # 2k - rating_gain(...)

if __name__ in "__main__":
    for mode in ("Normal", "Killer"):
        for board_size in (4, 6, 9, 12, 16):
            for difficulty in ("Easy", "Medium", "Hard", "Expert"):
                t = average_time_to_complete(mode, board_size, difficulty)
                print(f"{mode} {board_size} {difficulty} : {t // 60}m {t % 60}s")


'''
v1
Normal 4 Easy : 0m 47s
Normal 4 Medium : 1m 59s
Normal 4 Hard : 3m 57s
Normal 4 Expert : 7m 54s
Normal 6 Easy : 1m 47s
Normal 6 Medium : 4m 27s
Normal 6 Hard : 8m 53s
Normal 6 Expert : 17m 47s
Normal 9 Easy : 4m 0s
Normal 9 Medium : 10m 0s
Normal 9 Hard : 20m 0s
Normal 9 Expert : 40m 0s
Normal 12 Easy : 7m 7s
Normal 12 Medium : 17m 47s
Normal 12 Hard : 35m 33s
Normal 12 Expert : 71m 7s
Normal 16 Easy : 12m 39s
Normal 16 Medium : 31m 36s
Normal 16 Hard : 63m 13s
Normal 16 Expert : 126m 25s
Killer 4 Easy : 0m 47s
Killer 4 Medium : 2m 22s
Killer 4 Hard : 4m 56s
Killer 4 Expert : 9m 53s
Killer 6 Easy : 1m 47s
Killer 6 Medium : 5m 20s
Killer 6 Hard : 11m 7s
Killer 6 Expert : 22m 13s
Killer 9 Easy : 4m 0s
Killer 9 Medium : 12m 0s
Killer 9 Hard : 25m 0s
Killer 9 Expert : 50m 0s
Killer 12 Easy : 7m 7s
Killer 12 Medium : 21m 20s
Killer 12 Hard : 44m 27s
Killer 12 Expert : 88m 53s
Killer 16 Easy : 12m 39s
Killer 16 Medium : 37m 56s
Killer 16 Hard : 79m 1s
Killer 16 Expert : 158m 1s

v5
Normal 4 Easy : 0m 25s
Normal 4 Medium : 0m 26s
Normal 4 Hard : 0m 26s
Normal 4 Expert : 0m 27s
Normal 6 Easy : 0m 45s
Normal 6 Medium : 1m 2s
Normal 6 Hard : 1m 26s
Normal 6 Expert : 1m 59s
Normal 9 Easy : 4m 0s
Normal 9 Medium : 8m 41s
Normal 9 Hard : 18m 51s
Normal 9 Expert : 40m 54s
Normal 12 Easy : 7m 30s
Normal 12 Medium : 16m 32s
Normal 12 Hard : 36m 25s
Normal 12 Expert : 80m 14s
Normal 16 Easy : 12m 50s
Normal 16 Medium : 28m 42s
Normal 16 Hard : 64m 12s
Normal 16 Expert : 143m 36s
Killer 4 Easy : 0m 25s
Killer 4 Medium : 0m 26s
Killer 4 Hard : 0m 27s
Killer 4 Expert : 0m 28s
Killer 6 Easy : 0m 45s
Killer 6 Medium : 1m 13s
Killer 6 Hard : 1m 59s
Killer 6 Expert : 3m 14s
Killer 9 Easy : 4m 0s
Killer 9 Medium : 12m 48s
Killer 9 Hard : 40m 54s
Killer 9 Expert : 130m 49s
Killer 12 Easy : 7m 30s
Killer 12 Medium : 24m 32s
Killer 12 Hard : 80m 14s
Killer 12 Expert : 262m 25s
Killer 16 Easy : 12m 50s
Killer 16 Medium : 42m 56s
Killer 16 Hard : 143m 36s
Killer 16 Expert : 480m 22s
'''