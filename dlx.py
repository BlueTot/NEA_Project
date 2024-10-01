from itertools import product  # import product function


'''
###########################################################################################
# GROUP A Skill: Dancing Links X Algorithm used to solve Normal Sudoku boards             #
#                                                                                         #
# The Game and Board classes both use a recursive algorithm called DLX, which is a fast   #
# recursive depth-first backtracking solver used to solve normal sudoku boards.           #
# It takes in a NormalModeBoard object and returns a solved version of that board object. #
###########################################################################################
'''
class DLXSolver:  # Dancing Links X Solver class

    @staticmethod
    def solve_sudoku(board):  # Main solver function (takes NormalModeBoard object)

        N = board.board_size  # Board size constant

        cols = ([("row col", row_col) for row_col in
                 product(range(N), range(N))] +  # Constraint 1: each cell must have a number in it
                [("row num", row_num) for row_num in
                 product(range(N), range(1, N + 1))] +  # Constraint 2: each different number must appear in every row
                [("col num", col_num) for col_num in
                 product(range(N), range(1, N + 1))] +  # Contraint 3: each different number must appear in every column
                [("matrix num", matrix_num) for matrix_num in product(range(N), range(1,
                                                                                      N + 1))])  # Constraint 4: each different number must appear in every matrix/box

        
        '''
        #####################################################################################################################################################
        # GROUP A Skill: Dictionaries - used by the DLX algorithm to solve sudoku boards quickly.                                                           #
        # This is not the only place dictionaries are used, other places like group_colouring.py, ratin_calc.py, difficulty_settings.py etc. also use them. #
        #                                                                                                                                                   #
        # Dictionaries are frequently used in many areas of the code, mainly used by the Dancing Links Solver in dlx.py, and used to store groups in Killer #
        # Sudoku boards in board.py and used to underpin an adjacency list for graph traversal in the Group Colouring algorithm in group_colouring.py.      #
        # In other smaller files such as rating_calc.py and difficulty_settings.py, dictionaries are used to store constants that are used by some areas    #
        # of the program, such as storing the recommended ratings of each difficulty to calculate rating gain/losses for the user, and storing the number   #
        # of given numbers for each difficulty, used by the board generator algorithm.                                                                      #
        #####################################################################################################################################################
        '''
        rows = {}  # Initialise rows dictionary
        for row, col, num in product(range(N), range(N), range(1, N + 1)):
            # Populate rows dictionary with the columns that they match
            matrix_num = board.matrix_num(row, col)
            rows[(row, col, num)] = [("row col", (row, col)),
                                     ("row num", (row, num)),
                                     ("col num", (col, num)),
                                     ("matrix num", (matrix_num, num))]

        cols, rows = DLXSolver.__convert_to_sets(cols,
                                                 rows)  # Convert cols into dictionary of sets for easy access from cols to rows

        for rowidx, row in enumerate(board.board):  # Iterate through all squares of the given board
            for colidx, sq in enumerate(row):
                if sq.num:  # If the number at the square is not 0
                    '''
                    Uses the COVER function to eliminate all other possibilites for that square as any other possibilities 
                    with one or more identical constraints would be eliminated
                    E.g. if the number 1 is in the (0, 0) square, COVER would remove any possibilities with:
                    1. a number in the square (0, 0)
                    2. the number 1 in the first row
                    3. the number 1 in the first column
                    4. the number 1 in the first matrix/box
                    '''
                    DLXSolver.__cover(cols, rows, (rowidx, colidx, sq.num))

        for solution_set in DLXSolver.__solve(cols,
                                              rows):  # Iterate through all solutions of the board using DLX Solver
            for (row, col, num) in solution_set:  # Iterate through all squares
                board.set_num_at(row, col, num)
            yield board  # Return a copy of the board and continue looping thorugh all solutions

    @staticmethod
    def __convert_to_sets(cols, rows):  # Function to convert set to dictionary of sets for fast access
        cols = {col: set() for col in cols}  # Setup dictionary
        for row_id, row_contents in rows.items():  # Loop through rows
            for col in row_contents:  # Loop through cols
                cols[col].add(row_id)  # Add row to set
        return cols, rows  # Return dictionaries

    @staticmethod
    def __solve(cols, rows, solution_set=[]):  # Dancing Links X main solver algorithm
        if not cols:  # Check if no more columns left in the matrix (base case)
            return [list(solution_set)]  # Return the solution set
        else:
            min_col = min(cols, key=lambda col: len(
                cols[col]))  # Get column with least number of intersecting rows (S-heuristic)
            sols = []  # Initialise list of solution sets
            for selected_row in list(cols[min_col]):  # Iterate thorugh rows, selecting a row to cover every time
                solution_set.append(selected_row)  # Add to solution set
                cols, cells_to_restore = DLXSolver.__cover(cols, rows,
                                                           selected_row)  # Cover selected row and intersecting cols
                for sol in DLXSolver.__solve(cols, rows, solution_set):  # Recursively solve the reduced matrix
                    sols.extend([sol])  # Add solution set to list of solution sets
                cols = DLXSolver.__uncover(cols, cells_to_restore)  # Uncover
                solution_set.pop()  # Remove from solution set
            return sols  # return list of solution sets

    @staticmethod
    def __cover(cols, rows, selected_row):  # Cover function
        cells_to_restore = set()  # Initialise set of cells to restore for uncover function
        cols_to_remove = set()  # Initialise set of cols to remove
        for col_to_remove in rows[selected_row]:  # Iterate through cols to remove
            cols_to_remove.add(col_to_remove)  # Add col to set of cols to remove
            for row_to_remove in cols[col_to_remove]:  # Iterate through rows to remove
                for intersecting_col in rows[row_to_remove]:  # Iterate through intersecting column of the row
                    cells_to_restore.add((intersecting_col, row_to_remove))  # Add cell to set of cells to restore
        for col, row in cells_to_restore:  # Loop through cells to restore
            cols[col].remove(row)  # Remove the cell from the matrix
        for col in cols_to_remove:  # Loop through cols to remove
            cols.pop(col)  # Remove the col
        return cols, cells_to_restore  # Return the new cols dictionary and cells to restore (rows dictionary untouched, only connections removed)

    @staticmethod
    def __uncover(cols, cells_to_restore):  # Uncover function
        for col, row in cells_to_restore:  # Loop through cells to restore
            if col not in cols:  # If col has been removed
                cols[col] = set()  # Restore the set
            cols[col].add(row)  # Now add the row back to the set
        return cols  # Return the restored cols dictionary
