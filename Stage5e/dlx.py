from itertools import product

def solve_sudoku(size, grid):
    """ An efficient Sudoku solver using Algorithm X.

    >>> grid = [
    ...     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ...     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    ...     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    ...     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    ...     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    ...     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    ...     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    ...     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    ...     [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    >>> for solution in solve_sudoku((3, 3), grid):
    ...     print(*solution, sep='\\n')
    [5, 3, 4, 6, 7, 8, 9, 1, 2]
    [6, 7, 2, 1, 9, 5, 3, 4, 8]
    [1, 9, 8, 3, 4, 2, 5, 6, 7]
    [8, 5, 9, 7, 6, 1, 4, 2, 3]
    [4, 2, 6, 8, 5, 3, 7, 9, 1]
    [7, 1, 3, 9, 2, 4, 8, 5, 6]
    [9, 6, 1, 5, 3, 7, 2, 8, 4]
    [2, 8, 7, 4, 1, 9, 6, 3, 5]
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
    """
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

if __name__ == "__main__":
    board = [[4, 0, 0, 0, 0, 6, 0, 0, 2], [9, 3, 0, 0, 0, 7, 0, 1, 0], [0, 0, 0, 0, 0, 0, 7, 4, 3], [0, 0, 3, 1, 0, 0, 0, 5, 0], [0, 8, 0, 9, 0, 4, 0, 0, 0], [0, 0, 5, 0, 3, 0, 8, 0, 0], [0, 6, 0, 0, 0, 5, 0, 0, 0], [0, 2, 0, 0, 7, 0, 9, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0]]

    for sol in solve_sudoku((3, 3), board):
        print(sol)

'''
[[4, 0, 0, 0, 0, 6, 0, 0, 2], [9, 3, 0, 0, 0, 7, 0, 1, 0], [0, 0, 0, 0, 0, 0, 7, 4, 3], [0, 0, 3, 1, 0, 0, 0, 5, 0], [0, 8, 0, 9, 0, 4, 0, 0, 0], [0, 0, 5, 0, 3, 0, 8, 0, 0], [0, 6, 0, 0, 0, 5, 0, 0, 0], [0, 2, 0, 0, 7, 0, 9, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0]]
[[7, 7, 1, 3, 8, 6, 5, 9, 2], [9, 3, 2, 5, 4, 7, 6, 1, 8], [8, 5, 6, 2, 1, 9, 7, 4, 3], [2, 9, 3, 6, 6, 8, 4, 7, 7], [6, 7, 7, 7, 5, 2, 3, 2, 1], [1, 4, 5, 7, 3, 2, 8, 6, 9], [7, 6, 9, 8, 2, 3, 1, 3, 4], [3, 2, 4, 6, 6, 1, 9, 8, 5], [5, 1, 7, 4, 9, 3, 2, 7, 6]]
'''