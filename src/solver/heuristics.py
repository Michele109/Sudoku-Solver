from ..utils.validation import infer_block_size


def _get_available_values(grid, row, col, GRID_SIZE, BLOCK_SIZE):
    """Return valid values for an empty cell."""
    if grid[row][col] != 0:
        return []

    used_values = set()

    for value in grid[row]:
        if value != 0:
            used_values.add(value)

    for r in range(GRID_SIZE):
        value = grid[r][col]
        if value != 0:
            used_values.add(value)

    start_row = row - row % BLOCK_SIZE
    start_col = col - col % BLOCK_SIZE
    for r in range(start_row, start_row + BLOCK_SIZE):
        for c in range(start_col, start_col + BLOCK_SIZE):
            value = grid[r][c]
            if value != 0:
                used_values.add(value)

    return [value for value in range(1, GRID_SIZE + 1) if value not in used_values]


def find_empty_location(grid, GRID_SIZE=None, BLOCK_SIZE=None):
    """
    Finds the empty cell with the minimum number of remaining possible values (MRV heuristic).
    In case of a tie, uses the Degree heuristic to select the cell with the highest degree.
    Returns (row, column) of the cell with MRV/Degree, or None if there are no empty cells.
    """
    if GRID_SIZE is None:
        GRID_SIZE = len(grid)
    if BLOCK_SIZE is None:
        BLOCK_SIZE = infer_block_size(GRID_SIZE)
    min_remaining_values = GRID_SIZE + 1 # Max possible values for a cell is GRID_SIZE
    best_cell = None
    max_degree = -1 # Used for tie-breaking

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0: # If the cell is empty
                current_remaining_values = len(
                    _get_available_values(grid, r, c, GRID_SIZE, BLOCK_SIZE)
                )

                if current_remaining_values == 0:
                    return (r, c)

                if current_remaining_values < min_remaining_values: # New best cell for MRV
                    min_remaining_values = current_remaining_values
                    best_cell = (r, c)
                    max_degree = calculate_degree(
                        grid, r, c, GRID_SIZE=GRID_SIZE, BLOCK_SIZE=BLOCK_SIZE
                    ) # Calculate degree for this new best cell
                elif current_remaining_values == min_remaining_values: # MRV tie, use Degree
                    current_degree = calculate_degree(
                        grid, r, c, GRID_SIZE=GRID_SIZE, BLOCK_SIZE=BLOCK_SIZE
                    )
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
        BLOCK_SIZE = infer_block_size(GRID_SIZE)
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
        BLOCK_SIZE = infer_block_size(GRID_SIZE)

    valid_values = _get_available_values(grid, row, col, GRID_SIZE, BLOCK_SIZE)
    if len(valid_values) <= 1:
        return valid_values

    potential_values_with_lcv_score = []
    affected_cells = set()

    for c_affected in range(GRID_SIZE):
        affected_cells.add((row, c_affected))
    for r_affected in range(GRID_SIZE):
        affected_cells.add((r_affected, col))

    start_row = row - row % BLOCK_SIZE
    start_col = col - col % BLOCK_SIZE
    for r_block in range(start_row, start_row + BLOCK_SIZE):
        for c_block in range(start_col, start_col + BLOCK_SIZE):
            affected_cells.add((r_block, c_block))

    affected_cells.discard((row, col))

    for num_to_try in valid_values:
        # Temporarily place the number
        grid[row][col] = num_to_try
        options_left_for_neighbors = 0

        for r_neighbor, c_neighbor in affected_cells:
            if grid[r_neighbor][c_neighbor] == 0: # If the neighbor is empty
                options_left_for_neighbors += len(
                    _get_available_values(
                        grid, r_neighbor, c_neighbor, GRID_SIZE, BLOCK_SIZE
                    )
                )

        potential_values_with_lcv_score.append((options_left_for_neighbors, num_to_try))
        grid[row][col] = 0 # Revert temporary placement

    # Sort in descending order of options_left_for_neighbors (more options left is better)
    potential_values_with_lcv_score.sort(key=lambda x: x[0], reverse=True)
    return [num for _, num in potential_values_with_lcv_score]
