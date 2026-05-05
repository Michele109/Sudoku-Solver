from src.solver.validation import is_valid, is_valid_solution


def solved_grid(size: int):
    block = int(size ** 0.5)
    return [[((r * block + r // block + c) % size) + 1 for c in range(size)] for r in range(size)]


def test_is_valid_accepts_correct_move_9x9():
    grid = solved_grid(9)
    grid[0][0] = 0

    assert is_valid(grid, 0, 0, 1)
    assert not is_valid(grid, 0, 0, 2)


def test_is_valid_rejects_row_column_and_block_conflicts_16x16():
    grid = solved_grid(16)
    grid[0][0] = 0

    assert not is_valid(grid, 0, 0, grid[0][1])
    assert not is_valid(grid, 0, 0, grid[1][0])
    assert not is_valid(grid, 0, 0, grid[1][1])


def test_is_valid_solution_accepts_9x9_and_16x16():
    assert is_valid_solution(solved_grid(9))
    assert is_valid_solution(solved_grid(16))


def test_is_valid_solution_rejects_duplicate_value():
    grid = solved_grid(9)
    grid[0][0] = grid[0][1]

    assert not is_valid_solution(grid)
