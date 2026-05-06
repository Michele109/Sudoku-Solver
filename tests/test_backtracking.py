from conftest import solved_grid

from src.solver.backtraking import SolverStats, solve_sudoku, solve_sudoku_with_stats


def test_solve_sudoku_solves_single_missing_cell_9x9():
    grid = solved_grid(9)
    grid[0][0] = 0

    assert solve_sudoku(grid)
    assert grid == solved_grid(9)


def test_solve_sudoku_solves_single_missing_cell_16x16():
    grid = solved_grid(16)
    grid[5][11] = 0

    assert solve_sudoku(grid)
    assert grid == solved_grid(16)


def test_solve_sudoku_updates_stats_when_provided():
    grid = solved_grid(9)
    grid[0][0] = 0

    stats = SolverStats()
    assert solve_sudoku(grid, stats=stats)

    assert stats.recursive_calls >= 2
    assert stats.nodes_expanded >= 1
    assert stats.nodes_generated >= 1
    assert stats.max_depth >= 1
    assert stats.solutions_found == 1


def test_solve_sudoku_with_stats_returns_stats():
    grid = solved_grid(9)
    grid[8][8] = 0

    solved, stats = solve_sudoku_with_stats(grid)

    assert solved
    assert grid == solved_grid(9)
    assert isinstance(stats, SolverStats)
    assert stats.nodes_generated >= 1
