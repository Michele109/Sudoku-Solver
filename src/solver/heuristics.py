from .validation import is_valid

def find_empty_location(grid, GRID_SIZE=None):
    """
    Finds the empty cell with the minimum number of remaining possible values (MRV heuristic).
    In case of a tie, uses the Degree heuristic to select the cell with the highest degree.
    Returns (row, column) of the cell with MRV/Degree, or None if there are no empty cells.
    """
    if GRID_SIZE is None:
        GRID_SIZE = len(grid)
    min_remaining_values = GRID_SIZE + 1 # Max possible values for a cell is GRID_SIZE
    best_cell = None
    max_degree = -1 # Used for tie-breaking

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0: # If the cell is empty
                current_remaining_values = 0
                for num_to_try in range(1, GRID_SIZE + 1): # Numbers from 1 to 16
                    if is_valid(grid, r, c, num_to_try):
                        current_remaining_values += 1

                if current_remaining_values < min_remaining_values: # New best cell for MRV
                    min_remaining_values = current_remaining_values
                    best_cell = (r, c)
                    max_degree = calculate_degree(grid, r, c) # Calculate degree for this new best cell
                elif current_remaining_values == min_remaining_values: # MRV tie, use Degree
                    current_degree = calculate_degree(grid, r, c)
                    if current_degree > max_degree: # This cell has a higher degree
                        best_cell = (r, c)
                        max_degree = current_degree
    return best_cell

def calculate_degree(grid, row, col, GRID_SIZE=None, BLOCK_SIZE=None):
    """
    Calculates the 'degree' of an empty cell, which is the number of empty cells
    in the same row, column, or 4x4 block.
    """
    if GRID_SIZE is None:
        GRID_SIZE = len(grid)
    if BLOCK_SIZE is None:
        import math
        BLOCK_SIZE = int(math.isqrt(GRID_SIZE))
    degree = 0
    # Row
    for x in range(GRID_SIZE):
        if grid[row][x] == 0 and x != col:
            degree += 1
    # Column
    for x in range(GRID_SIZE):
        if grid[x][col] == 0 and x != row:
            degree += 1
    # 4x4 Block
    start_row = row - row % BLOCK_SIZE
    start_col = col - col % BLOCK_SIZE
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            if grid[i + start_row][j + start_col] == 0 and not (i + start_row == row and j + start_col == col):
                degree += 1
    return degree

def get_lcv_ordered_values(grid, row, col, GRID_SIZE=None, BLOCK_SIZE=None):
    """
    Returns a list of numbers (1-16) ordered by the Least Constraining Value (LCV) heuristic.
    For each valid number, it calculates how many choices it leaves for other
    empty cells in the same row, column, or 4x4 block.
    Values that leave more choices are prioritized (least constraining).
    """
    if GRID_SIZE is None:
        GRID_SIZE = len(grid)
    if BLOCK_SIZE is None:
        import math
        BLOCK_SIZE = int(math.isqrt(GRID_SIZE))
    potential_values_with_lcv_score = []

    for num_to_try in range(1, GRID_SIZE + 1): # Numbers from 1 to 16
        if is_valid(grid, row, col, num_to_try, GRID_SIZE=GRID_SIZE, BLOCK_SIZE=BLOCK_SIZE):
            # Temporarily place the number
            grid[row][col] = num_to_try
            options_left_for_neighbors = 0

            # Check affected cells (same row, column, and 4x4 block)
            affected_cells = set()
            # Add cells in the same row
            for c_affected in range(GRID_SIZE):
                affected_cells.add((row, c_affected))
            # Add cells in the same column
            for r_affected in range(GRID_SIZE):
                affected_cells.add((r_affected, col))
            # Add cells in the same 4x4 block
            start_row = row - row % BLOCK_SIZE
            start_col = col - col % BLOCK_SIZE
            for r_block in range(start_row, start_row + BLOCK_SIZE):
                for c_block in range(start_col, start_col + BLOCK_SIZE):
                    affected_cells.add((r_block, c_block))

            # Exclude the current cell itself
            if (row, col) in affected_cells:
                affected_cells.remove((row, col))

            for r_neighbor, c_neighbor in affected_cells:
                if grid[r_neighbor][c_neighbor] == 0: # If the neighbor is empty
                    # Count valid options for this neighbor given the temporary placement
                    for val_option in range(1, GRID_SIZE + 1): # Numbers from 1 to 16
                        if is_valid(grid, r_neighbor, c_neighbor, val_option, GRID_SIZE=GRID_SIZE, BLOCK_SIZE=BLOCK_SIZE):
                            options_left_for_neighbors += 1

            potential_values_with_lcv_score.append((options_left_for_neighbors, num_to_try))
            grid[row][col] = 0 # Revert temporary placement

    # Sort in descending order of options_left_for_neighbors (more options left is better)
    potential_values_with_lcv_score.sort(key=lambda x: x[0], reverse=True)
    return [num for _, num in potential_values_with_lcv_score]