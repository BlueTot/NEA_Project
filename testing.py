from Stage4.board import BoardGenerator as S4BG
from time import perf_counter

times = []
for _ in range(10000):
    if _ % 100 == 0:
        print(_)
    stime = perf_counter()
    board = S4BG.new_board("Easy")
    times.append(perf_counter() - stime)
print("stage 4: ", sum(times)/len(times))

from Stage5a.board import BoardGenerator as S5ABG
from time import perf_counter

times2 = []
for _ in range(10000):
    if _ % 100 == 0:
        print(_)
    stime = perf_counter()
    board = S5ABG.new_board("Easy")
    times2.append(perf_counter() - stime)
print("stage 5a: ", sum(times2)/len(times2))



