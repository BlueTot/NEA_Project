# arr = [[1, 0, 0, 0, 0, 7, 0, 9, 0],
#        [0, 3, 0, 0, 2, 0, 0, 0, 8],
#        [0, 0, 9, 6, 0, 0, 5, 0, 0],
#        [0, 0, 5, 3, 0, 0, 9, 0, 0],
#        [0, 1, 0, 0, 8, 0, 0, 0, 2],
#        [6, 0, 0, 0, 0, 4, 0, 0, 0],
#        [3, 0, 0, 0, 0, 0, 0, 1, 0],
#        [0, 4, 0, 0, 0, 0, 0, 0, 7],
#        [0, 0, 7, 0, 0, 0, 3, 0, 0]]

arr = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 3, 6, 0, 0, 0, 0, 0],
       [0, 7, 0, 0, 9, 0, 2, 0, 0],
       [0, 5, 0, 0, 0, 7, 0, 0, 0],
       [0, 0, 0, 0, 4, 5, 7, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 3, 0],
       [0, 0, 1, 0, 0, 0, 0, 6, 8],
       [0, 0, 8, 5, 0, 0, 0, 1, 0],
       [0, 9, 0, 0, 0, 0, 4, 0, 0]]

row_digits = [0 for _ in range(9)]
col_digits = [0 for _ in range(9)]
matrix_digits = [0 for _ in range(9)]

def matrix_num(row, col):
    return 3 * (row // 3) + col // 3

sq_hash = ";".join([";".join([f"{num}," for num in row]) for row in arr])

for row in range(9):
    for col in range(9):
          num = arr[row][col]
          if num > 0:
            row_digits[row] += 2 ** (num - 1)
            col_digits[col] += 2 ** (num - 1)
            matrix_digits[matrix_num(row, col)] += 2 ** (num - 1)

digits_hash = ";".join([",".join([str(n) for n in row_digits]), ",".join([str(n) for n in col_digits]), ",".join([str(n) for n in matrix_digits])])
print(sq_hash + "/" + digits_hash)