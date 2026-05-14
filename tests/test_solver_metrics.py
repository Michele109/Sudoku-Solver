from src.solver.backtraking import SudokuSolver

def _solved_grid(size: int):
    block = int(size ** 0.5)
    return [[((r * block + r // block + c) % size) + 1 for c in range(size)] for r in range(size)]

def _grid_to_string(grid):
    chars = []
    for row in grid:
        for value in row:
            chars.append(str(value) if value <= 9 else chr(value - 10 + ord("A")))
    return "".join(chars)


def test_solver_solves_9x9_and_16x16_and_exposes_metrics():
    for size in (9, 16):
        grid = _solved_grid(size)
        grid[0][0] = 0

        solver = SudokuSolver(_grid_to_string(grid))

        assert solver.solve()
        assert solver.get_solution()[1] == _grid_to_string(_solved_grid(size))
        assert solver.expanded_nodes >= 1
        assert solver.max_memory_nodes >= 1
        assert solver.current_recursion_depth == 0


def test_solver_runs_constraint_propagation_during_recursive_search():
    class CountingSolver(SudokuSolver):
        def __init__(self, sudoku_string: str):
            self.propagation_calls = 0
            super().__init__(sudoku_string)

        def _apply_constraint_propagation(self):
            self.propagation_calls += 1
            return super()._apply_constraint_propagation()

    grid = _solved_grid(9)
    for row, col in [
        (6, 7), (7, 4), (8, 5), (7, 1), (8, 4), (0, 7),
        (1, 6), (6, 4), (3, 1), (6, 1), (7, 7),
    ]:
        grid[row][col] = 0
    solver = CountingSolver(_grid_to_string(grid))

    assert solver.solve()
    assert solver.propagation_calls >= 2
