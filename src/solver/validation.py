def is_valid(grid, row, col, num, GRID_SIZE=None, BLOCK_SIZE=None):
    """
    General validity check for placing `num` at (row, col) in `grid`.
    If GRID_SIZE or BLOCK_SIZE aren't provided they are inferred from the grid.
    Returns True if placement is valid, False otherwise.
    """
    # Infer sizes if not provided
    if GRID_SIZE is None:
        GRID_SIZE = len(grid)
    if BLOCK_SIZE is None:
        # Try to infer block size as integer square root
        import math
        bs = int(math.isqrt(GRID_SIZE))
        if bs * bs != GRID_SIZE:
            raise ValueError(f"Unsupported GRID_SIZE: {GRID_SIZE}")
        BLOCK_SIZE = bs

    # Basic bounds checks
    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        return False

    # Check row
    for x in range(GRID_SIZE):
        if grid[row][x] == num:
            return False

    # Check column
    for x in range(GRID_SIZE):
        if grid[x][col] == num:
            return False

    # Check block
    start_row = row - row % BLOCK_SIZE
    start_col = col - col % BLOCK_SIZE
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True
