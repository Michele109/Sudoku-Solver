import copy

from conftest import solved_grid
from src.utils.validation import is_valid, is_valid_solution, verify_integrity


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

def test_verify_integrity_accepts_valid_solution():
    """A correctly solved grid must pass verify_integrity."""
    original = solved_grid(9)
    original[4][4] = 0  # one empty cell in the original
    solved = copy.deepcopy(original)
    # Fill the empty cell with the correct value
    solved[4][4] = solved_grid(9)[4][4]

    assert verify_integrity(original, solved)

def test_verify_integrity_rejects_mutated_given_cell():
    """If a pre-filled cell in the original is changed in the solution, it must fail."""
    original = solved_grid(9)
    solved = copy.deepcopy(original)
    # Change a cell that was filled in the original
    solved[0][0] = (original[0][0] % 9) + 1  # a different value

    assert not verify_integrity(original, solved)

def test_verify_integrity_rejects_invalid_solution():
    """A grid that violates Sudoku rules must fail even if given cells are intact."""
    original = solved_grid(9)
    original[0][0] = 0  # one empty cell
    solved = copy.deepcopy(original)
    # Fill the empty cell with an invalid (duplicate) value
    solved[0][0] = solved[0][1]

    assert not verify_integrity(original, solved)

def test_verify_integrity_accepts_fully_prefilled_solved_grid():
    """A grid with no empty cells that is valid should pass."""
    original = solved_grid(9)
    solved = copy.deepcopy(original)

    assert verify_integrity(original, solved)

def test_verify_integrity_accepts_16x16():
    """verify_integrity must work correctly for 16x16 grids."""
    original = solved_grid(16)
    original[0][0] = 0
    solved = copy.deepcopy(original)
    solved[0][0] = solved_grid(16)[0][0]

    assert verify_integrity(original, solved)
