from math import exp, e, log # Import e^x function, e constant and ln function

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

AVERAGE_TIMES = {"Normal": {"Easy": 4*60, "Medium": 10*60, "Hard": 20*60, "Expert": 40*60},
                 "Killer": {"Easy": 4*60, "Medium": 12*60, "Hard": 25*60, "Expert": 50*60}}

def average_time(mode, board_size, difficulty):
    return round(AVERAGE_TIMES[mode][difficulty] / (9**2) * (board_size**2))

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
XP_PER_RUN = 20 # k

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
def rating_gain(mode, board_size, difficulty, rating, time):
    base_rating = __rating_gain(mode, board_size, difficulty, rating) # R
    t_avg = average_time(mode, board_size, difficulty) # T
    return round(5*base_rating/3 * exp(-log(2.5)/t_avg * time) + base_rating / 3) # 5R/3 * e^(-ln(2.5)/T * t) + R/3

'''RATING FORMULA: y = 2k - rating_gain(...)'''
def rating_loss(mode, board_size, difficulty, rating):
    return 2*XP_PER_RUN - __rating_gain(mode, board_size, difficulty, rating) # 2k - rating_gain(...)
