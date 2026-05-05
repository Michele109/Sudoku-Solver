from src.solver.backtraking import solve_sudoku


def solved_grid(size: int):
    block = int(size ** 0.5)
    return [[((r * block + r // block + c) % size) + 1 for c in range(size)] for r in range(size)]


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
