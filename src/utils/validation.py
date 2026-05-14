import pandas as pd
import math

from src.utils.constants import SUPPORTED_GRID_SIZES

def is_valid(grid: list, row: int, col: int, num: int, GRID_SIZE=None, BLOCK_SIZE=None) -> bool:
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


def verify_integrity(original_grid: list, solved_grid: list):
    """
    Verifies that a solved grid is a valid, complete Sudoku solution that
    is consistent with the original (unsolved) puzzle.
    """
    GRID_SIZE = len(original_grid)

    # Immutability check: pre-filled cells must be unchanged
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if original_grid[r][c] != 0 and original_grid[r][c] != solved_grid[r][c]:
                return False

    # Rule consistency check
    return is_valid_solution(solved_grid)


def is_valid_solution(grid: list) -> bool:
    """
    Checks if a given Sudoku grid is a valid solution.
    Supports both 9x9 and 16x16 grids (or any square size).
    A grid is valid if each row, each column, and each subgrid
    contains all the digits from 1 to GRID_SIZE without repetition.
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

def infer_block_size(grid_size: int) -> int:
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


def verify_sudoku_solution(row_data: pd.Series):
      """
      Verifies if the SudokuSolver finds the correct solution for a given row of data.
      """

      from src.solver.backtraking import SudokuSolver

      puzzle_str = row_data['Sudoku']
      expected_solution_str = row_data['solution']

      solver = SudokuSolver(puzzle_str)

      if solver.solve():

    # Convert the solved grid back to a single string for comparison
        found_solution_str = solver.get_solution()[1]

        is_correct = (found_solution_str == expected_solution_str)

        return (
        is_correct,
        solver.search_nodes,
        solver.propagation_assignments,
        solver.max_memory_nodes
        )
      else:
          return (
    False,
    solver.search_nodes,
    solver.propagation_assignments,
    solver.max_memory_nodes
)