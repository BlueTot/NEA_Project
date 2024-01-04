# from generator import BoardGenerator
#from time import perf_counter

# total = 0
# total2 = 0
# for _ in range(100):
#     print(_)
#     try:
#         board = BoardGenerator.new_board("Killer", "Easy", 12)
#         colours = board.group_colours()
#         if 4 in colours.values():
#             total += 1
#     except IndexError:
#         total2 += 1
# print(total)
# print(total2)

# original: 55 (5 colours), 3 (6+ colours)
# with no priority queue: 23
# with priority queue: 4

# board = BoardGenerator.new_board("Killer", "Easy", 6)
# print(board.group_colours())