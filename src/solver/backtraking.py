def is_valid(grid, row, col, num):
    GRID_SIZE = 16
    BLOCK_SIZE = 4

    # Check row
    for x in range(GRID_SIZE):
        if grid[row][x] == num:
            return False

    # Check column
    for x in range(GRID_SIZE):
        if grid[x][col] == num:
            return False

    # Check 4x4 block
    start_row = row - row % BLOCK_SIZE
    start_col = col - col % BLOCK_SIZE
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def solve_sudoku(grid):
    # Find the next empty cell using MRV heuristic with Degree tie-breaking
    empty_cell = find_empty_location(grid)
    if not empty_cell:
        return True # Sudoku solved!

    row, col = empty_cell

    # Use LCV to order the numbers to try
    lcv_ordered_nums = get_lcv_ordered_values(grid, row, col)

    # Try values in the domain {1...16} in LCV order
    for num in lcv_ordered_nums:
        if is_valid(grid, row, col, num):
            # Tentative assignment
            grid[row][col] = num

            # Recursion (DFS)
            if solve_sudoku(grid):
                return True

            # Failure: Backtrack (remove assignment)
            grid[row][col] = 0

    return False