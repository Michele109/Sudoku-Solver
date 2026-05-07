from src.solver.heuristics import calculate_degree, find_empty_location, get_lcv_ordered_values


def solved_grid(size: int):
    block = int(size ** 0.5)
    return [[((r * block + r // block + c) % size) + 1 for c in range(size)] for r in range(size)]


def test_find_empty_location_returns_single_missing_cell():
    grid = solved_grid(9)
    grid[4][7] = 0

    assert find_empty_location(grid) == (4, 7)


def test_calculate_degree_counts_empty_neighbors():
    grid = solved_grid(9)
    grid[4][7] = 0
    grid[4][1] = 0
    grid[0][7] = 0

    assert calculate_degree(grid, 4, 7) >= 2


def test_get_lcv_ordered_values_returns_only_valid_value_for_single_hole():
    grid = solved_grid(16)
    grid[0][0] = 0

    assert get_lcv_ordered_values(grid, 0, 0) == [1]


def test_find_empty_location_prioritizes_cell_with_no_candidates():
    grid = solved_grid(9)
    grid[0][0] = 0
    grid[8][8] = 0
    grid[1][0] = 1

    assert find_empty_location(grid) == (0, 0)
