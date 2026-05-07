from dataclasses import dataclass

from .heuristics import find_empty_location, get_lcv_ordered_values


@dataclass
class SolverStats:
    """Runtime stats collected during DFS backtracking."""

    recursive_calls: int = 0
    nodes_expanded: int = 0
    nodes_generated: int = 0
    backtracks: int = 0
    max_depth: int = 0
    solutions_found: int = 0

def solve_sudoku(grid, stats=None, _depth=0, _grid_size=None, _block_size=None):
    if _grid_size is None:
        _grid_size = len(grid)
    if _block_size is None:
        _block_size = int(_grid_size ** 0.5)

    if stats is not None:
        stats.recursive_calls += 1
        stats.max_depth = max(stats.max_depth, _depth)

    # Find the next empty cell using MRV heuristic with Degree tie-breaking
    empty_cell = find_empty_location(grid, GRID_SIZE=_grid_size, BLOCK_SIZE=_block_size)
    if not empty_cell:
        if stats is not None:
            stats.solutions_found += 1
        return True # Sudoku solved!

    if stats is not None:
        stats.nodes_expanded += 1

    row, col = empty_cell

    # Use LCV to order the numbers to try
    lcv_ordered_nums = get_lcv_ordered_values(
        grid, row, col, GRID_SIZE=_grid_size, BLOCK_SIZE=_block_size
    )

    # Try values in the domain {1...16} in LCV order
    for num in lcv_ordered_nums:
        if stats is not None:
            stats.nodes_generated += 1

        # Tentative assignment
        grid[row][col] = num

        # Recursion (DFS)
        if solve_sudoku(
            grid,
            stats=stats,
            _depth=_depth + 1,
            _grid_size=_grid_size,
            _block_size=_block_size,
        ):
            return True

        # Failure: Backtrack (remove assignment)
        grid[row][col] = 0
        if stats is not None:
            stats.backtracks += 1

    return False


def solve_sudoku_with_stats(grid):
    """Solves the grid and returns (solved, stats)."""

    stats = SolverStats()
    solved = solve_sudoku(grid, stats=stats)
    return solved, stats
