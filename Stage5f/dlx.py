'''
WARNING: This code is not completely written by myself, most of the algorithmic structure is
based off https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html by Ali Assaf <ali.assaf.mail@gmail.com>
'''

from itertools import product
from copy import deepcopy

class DLXSolver:
    
    @staticmethod
    def solve_sudoku(board): # Main solver function (takes NormalModeBoard object)

        n = board.board_size # board size
        cols = ([("row col", rc) for rc in product(range(n), repeat=2)] + # Constraint 1: each cell must have a number in it
                [("row num", rn) for rn in product(range(n), range(1, n+1))] + # Constraint 2: each different number must appear in every row
                [("col num", cn) for cn in product(range(n), range(1, n+1))] + # Contraint 3: each different number must appear in every column
                [("matrix num", mn) for mn in product(range(n), range(1, n+1))]) # Constraint 4: each different number must appear in every matrix/box
        
        rows = {}
        for row, col, num in product(range(n), range(n), range(1, n+1)):
            rows[(row, col, num)] = [("row col", (row, col)), ("row num", (row, num)), 
                                  ("col num", (col, num)), ("matrix num", (board.matrix_num(row, col), num))] # Populate rows dictionary with the columns that they match
            
        cols, rows = DLXSolver.convert_to_sets(cols, rows) # Convert cols into dictionary of sets for easy access from cols to rows

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
                    DLXSolver.cover(cols, rows, (rowidx, colidx, sq.num))

        for solution_set in DLXSolver.dlx_solve(cols, rows): # Iterate through all solutions of the board using DLX Solver
            for row, col, num in solution_set: # Iterate through all squares
                board.set_num_at(row, col, num) # Set num at square
            yield deepcopy(board) # Return a copy of the board

    # Convert representation of cols from a set to a dict to give fast access from the columns to the rows
    @staticmethod
    def convert_to_sets(cols, rows): 
        cols = {col : set() for col in cols}
        for row_id, row_contents in rows.items():
            for col in row_contents:
                cols[col].add(row_id)
        return cols, rows
    
    @staticmethod
    def dlx_solve(cols, rows, solution_set=[]):
        if not cols: # no remaining columns (constraints)
            yield solution_set # return solution set
        else:
            chosen_col = min(cols, key=lambda col : len(cols[col])) # Select column with least 1s (S-heuristic)
            for chosen_row in cols[chosen_col]: # Iterate through all rows that intersect with the chosen column
                solution_set.append(chosen_row) # add this row to the solution set
                # cover columns (rows remain intact so uncovering is easier, only the connections from the cols to the rows are removed)
                covered_cols = DLXSolver.cover(cols, rows, chosen_row) 
                for sol in DLXSolver.dlx_solve(cols, rows, solution_set): # recursively solve the reduced matrix
                    yield sol
                # uncover columns (the chosen row is used to obtain the cols that have been covered from the intact rows dictionary)
                DLXSolver.uncover(cols, rows, chosen_row, covered_cols)
                solution_set.pop() # remove this row from the solution set
    
    @staticmethod
    def cover(cols, rows, chosen_row): # cover columns function
        covered_cols = []
        for col in rows[chosen_row]: # iterate through columns to be covered
            for row in cols[col]: # iterate through intersecting rows of the columns to be covered
                for selected_col in rows[row]: # iterate through intersecting cols of that row
                    '''check if original constraint col is different to the col we are selecting 
                    (this is used to only remove row connections in other columns not our own column 
                    so we can remove it at the end and add to covered cols)'''
                    if col != selected_col: 
                        cols[selected_col].remove(row) # remove row connection from other cols (not the base col)
            covered_cols.append(cols.pop(col)) # finally now we remove the base row from cols and add to covered cols
        return covered_cols
    
    @staticmethod
    def uncover(cols, rows, chosen_row, covered_cols): # uncover columns function
        for col in reversed(rows[chosen_row]): # iterate through columns to be uncovered in reverse order
            cols[col] = covered_cols.pop() # add the row set stored back into cols
            for row in cols[col]: # iterate through intersecting rows of that col
                for selected_col in rows[row]: # iterate through intersecting cols of that row
                    if col != selected_col: # check if col is different to selected col, reasoning explained above in the multiline comment
                        cols[selected_col].add(row) # finally we populate the newly added row set with remaining rows
