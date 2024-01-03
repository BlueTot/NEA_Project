from itertools import product # Import product function from itertools

class DLXSolver: # Dancing Links X Sudoku Solver

    @staticmethod
    def solve_sudoku(board): # Public method called to solve sudoku, sets up the matrix for the DLX algorithm to solve

        N = board.board_size # Set board size constant

        # CREATE COLUMNS SET
        cols = set([("row col", rc) for rc in product(range(N), range(N))] + # Constraint 1: each cell must have a number in it
                [("row num", rn) for rn in product(range(N), range(1, N + 1))] + # Constraint 2: each different number must appear in every row
                [("col num", cn) for cn in product(range(N), range(1, N + 1))] + # Contraint 3: each different number must appear in every column
                [("matrix num", mn) for mn in product(range(N), range(1, N + 1))]) # Constraint 4: each different number must appear in every matrix/box
        
        # CREATE ROWS DICTIONARY
        rows = {}
        for row, col, num in product(range(N), range(N), range(1, N + 1)):
            # Populate rows dictionary with the columns that they match
            matrix_num = board.matrix_num(row, col) # Get matrix number of square
            rows[(row, col, num)] = [("row col", (row, col)), ("row num", (row, num)), ("col num", (col, num)), ("matrix num", (matrix_num, num))] 

        cols = DLXSolver.__convert_to_sets(cols, rows) # Convert cols into dictionary of sets for easy access from cols to rows

        for rowidx, row in enumerate(board.board): # Iterate through all squares of the given board
            for colidx, sq in enumerate(row):
                if sq.num: # If the number at the square is not 0
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

        for solution_set in DLXSolver.__solve(cols, rows): # Iterate through all solutions of the board using DLX Solver
            for (row, col, num) in solution_set: # Iterate through all squares
                board.set_num_at(row, col, num) # Set number at that square to be the correct number
            yield board # Return a copy of the board

    @staticmethod
    def __convert_to_sets(cols, rows): # Function to convert set to dictionary of sets for easy access from cols to rows
        cols = {col : set() for col in cols} # Initialise dictionary
        for row_id, row_contents in rows.items(): # Loop through rows
            for col in row_contents: # Loop through intersecting columns
                cols[col].add(row_id) # Add column to cols dictionary
        return cols # Return dictionary

    @staticmethod
    def __solve(cols, rows, solution_set=[]): # Dancing Links X main solver algorithm
        if not cols: # Return solution set when no columns left (base case)
            yield solution_set
        else:
            min_col = min(cols, key= lambda col : len(cols[col])) # Get column with least number of intersecting rows (S-heuristic)
            for selected_row in list(cols[min_col]): # Iterate thorugh rows, selecting a row to cover every time
                solution_set.append(selected_row) # Add to solution set
                cols, cells_to_restore = DLXSolver.__cover(cols, rows, selected_row) # Cover selected row and intersecting cols
                for sol in DLXSolver.__solve(cols, rows, solution_set): # Recursively solve the reduced matrix
                    yield sol
                cols = DLXSolver.__uncover(cols, cells_to_restore) # Uncover
                solution_set.pop() # Remove from solution set

    @staticmethod
    def __cover(cols, rows, selected_row): # Cover function
        cells_to_restore = set() # Initialise set of cells to restore for uncover function
        cols_to_remove = set() # Initialise set of cols to remove
        for col_to_remove in rows[selected_row]: # Iterate through cols to remove
            cols_to_remove.add(col_to_remove) # Add col to set of cols to remove
            for row_to_remove in cols[col_to_remove]: # Iterate through rows to remove
                for intersecting_col in rows[row_to_remove]: # Iterate through intersecting column of the row
                    cells_to_restore.add((intersecting_col, row_to_remove)) # Add cell to set of cells to restore
        for col, row in cells_to_restore: # Loop through cells to restore
            cols[col].remove(row) # Remove the cell from the matrix
        for col in cols_to_remove: # Loop through cols to remove
            cols.pop(col) # Remove the col
        return cols, cells_to_restore # Return the new cols dictionary and cells to restore (rows dictionary untouched, only connections removed)

    @staticmethod
    def __uncover(cols, cells_to_restore): # Uncover function
        for col, row in cells_to_restore: # Loop through cells to restore
            if col not in cols: # If col has been removed
                cols[col] = set() # Restore the set
            cols[col].add(row) # Now add the row back to the set
        return cols # Return the restored cols dictionary
