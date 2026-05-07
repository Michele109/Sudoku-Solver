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
        BLOCK_SIZE = infer_block_size(GRID_SIZE)

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


def verify_integrity(original_grid, solved_grid):
    """
    Verifies that a solved grid is a valid, complete Sudoku solution that
    is consistent with the original (unsolved) puzzle.

    Criteria:
    1. Immutability: every pre-filled (non-zero) cell in original_grid must
       retain the same value in solved_grid.
    2. Rule Consistency: every row, column, and sub-grid must contain each
       digit from 1 to GRID_SIZE exactly once (delegates to is_valid_solution).

    Args:
        original_grid: 2D list representing the original puzzle (0 = empty).
        solved_grid:   2D list representing the solver's proposed solution.

    Returns:
        bool: True if both criteria are satisfied, False otherwise.
    """
    GRID_SIZE = len(original_grid)

    # Immutability check: pre-filled cells must be unchanged
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if original_grid[r][c] != 0 and original_grid[r][c] != solved_grid[r][c]:
                return False

    # Rule consistency check
    return is_valid_solution(solved_grid)


def is_valid_solution(grid):
    """
    Checks if a given Sudoku grid is a valid solution.
    Supports both 9x9 and 16x16 grids (or any square size).
    A grid is valid if each row, each column, and each subgrid
    contains all of the digits from 1 to GRID_SIZE without repetition.
    """
    # Infer GRID_SIZE from the grid and compute BLOCK_SIZE
    GRID_SIZE = len(grid)
    BLOCK_SIZE = infer_block_size(GRID_SIZE)
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

"""Shared utilities for the solver module."""

import math

# Supported grid sizes
SUPPORTED_GRID_SIZES = (9, 16)


def infer_block_size(grid_size):
    """
    Infers the block size (e.g., 3 for 9x9, 4 for 16x16) from the grid size.
    
    Args:
        grid_size: The size of the Sudoku grid (9 or 16).
        
    Returns:
        int: The block size.
        
    Raises:
        ValueError: If grid_size is not a perfect square or not supported.
    """
    block_size = int(math.isqrt(grid_size))
    if block_size * block_size != grid_size:
        raise ValueError(f"Unsupported GRID_SIZE: {grid_size}. Must be a perfect square.")
    if grid_size not in SUPPORTED_GRID_SIZES:
        raise ValueError(f"Unsupported GRID_SIZE: {grid_size}. Supported sizes: {SUPPORTED_GRID_SIZES}")
    return block_size


def validate_grid_size(grid_size):
    """
    Validates that the provided grid size is supported.
    
    Args:
        grid_size: The size to validate.
        
    Raises:
        ValueError: If the grid size is not supported.
    """
    if grid_size not in SUPPORTED_GRID_SIZES:
        raise ValueError(f"Grid size must be one of {SUPPORTED_GRID_SIZES}, got {grid_size}")

