def x(board_size):
    for factor in range(int(board_size ** 0.5) + 1, 0, -1):
        if board_size % factor == 0:
            return tuple(sorted((factor, board_size // factor)))
print(x(6))
matrix_size = x(6)
def matrix_num(row, col):
    return matrix_size[0] * (row // matrix_size[0]) + col // matrix_size[1]
for row in range(6):
    for col in range(6):
        print(matrix_num(row, col), end=' ')
    print()