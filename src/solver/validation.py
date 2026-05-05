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


def is_valid_solution(grid):
    """
    Checks if a given Sudoku grid is a valid solution.
    Supports both 9x9 and 16x16 grids (or any square size).
    A grid is valid if each row, each column, and each subgrid
    contains all of the digits from 1 to GRID_SIZE without repetition.
    """
    # Infer GRID_SIZE from the grid and compute BLOCK_SIZE
    GRID_SIZE = len(grid)
    import math
    bs = int(math.isqrt(GRID_SIZE))
    if bs * bs != GRID_SIZE:
        raise ValueError(f"Unsupported GRID_SIZE: {GRID_SIZE}")
    BLOCK_SIZE = bs
    required_nums = set(range(1, GRID_SIZE + 1))

    # Check rows
    for r in range(GRID_SIZE):
        seen_in_row = set()
        for c in range(GRID_SIZE):
            num = grid[r][c]
            if num == 0: # A valid solution should not have empty cells
                return False
            if num in seen_in_row:
                return False
            seen_in_row.add(num)
        if seen_in_row != required_nums:
            return False

    # Check columns
    for c in range(GRID_SIZE):
        seen_in_col = set()
        for r in range(GRID_SIZE):
            num = grid[r][c]
            if num == 0:
                return False
            if num in seen_in_col:
                return False
            seen_in_col.add(num)
        if seen_in_col != required_nums:
            return False

    # Check 4x4 subgrids
    for block_row_start in range(0, GRID_SIZE, BLOCK_SIZE):
        for block_col_start in range(0, GRID_SIZE, BLOCK_SIZE):
            seen_in_block = set()
            for r_offset in range(BLOCK_SIZE):
                for c_offset in range(BLOCK_SIZE):
                    num = grid[block_row_start + r_offset][block_col_start + c_offset]
                    if num == 0:
                        return False
                    if num in seen_in_block:
                        return False
                    seen_in_block.add(num)
            if seen_in_block != required_nums:
                return False

    return True
