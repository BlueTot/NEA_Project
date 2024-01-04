class DLXSolver:

    @staticmethod
    def convert_to_sets(cols, rows): 
        cols = {col : set() for col in cols}
        for row_id, row_contents in rows.items():
            for col in row_contents:
                cols[col].add(row_id)
        return cols, rows

    @staticmethod
    def solve(cols, rows, solution_set): # Dancing Links X main solver algorithm
        if not cols: # Return solution set when no columns left (base case)
            print(list(solution_set))
            print([list(solution_set)])
            return [list(solution_set)]
        else:
            min_col = min(cols, key= lambda col : len(cols[col])) # Get column with least number of intersecting rows (S-heuristic)
            sols = []
            for selected_row in list(cols[min_col]): # Iterate thorugh rows, selecting a row to cover every time
                solution_set.append(selected_row) # Add to solution set
                cols, cells_to_restore = DLXSolver.__cover(cols, rows, selected_row) # Cover selected row and intersecting cols
                for sol in DLXSolver.solve(cols, rows, solution_set): # Recursively solve the reduced matrix
                    sols.extend([sol])
                cols = DLXSolver.__uncover(cols, cells_to_restore) # Uncover
                solution_set.pop() # Remove from solution set
            return sols

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
    
if __name__ in "__main__":

    cols = {1, 2, 3, 4, 5, 6, 7}
    rows = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}
    
    cols, rows = DLXSolver.convert_to_sets(cols, rows)
    for sol in DLXSolver.solve(cols, rows, []):
        print(sol)