from conftest import solved_grid
from src.solver.backtraking import SudokuSolver
from src.utils.visualizer import prepare_string_from_grid

def test_solve_sudoku_solves_single_missing_cell_9x9():
    # Prepariamo la griglia
    original_grid = solved_grid(9)
    solution_str = prepare_string_from_grid(original_grid)

    # Creiamo un puzzle con una cella mancante
    grid_with_hole = solved_grid(9)
    grid_with_hole[0][0] = 0
    puzzle_str = prepare_string_from_grid(grid_with_hole)

    solver = SudokuSolver(puzzle_str)

    assert solver.solve() is True
    assert solver.get_solution()[1] == solution_str


def test_solve_sudoku_solves_single_missing_cell_16x16():
    original_grid = solved_grid(16)
    solution_str = prepare_string_from_grid(original_grid)

    grid_with_hole = solved_grid(16)
    grid_with_hole[5][11] = 0
    puzzle_str = prepare_string_from_grid(grid_with_hole)

    solver = SudokuSolver(puzzle_str)

    assert solver.solve() is True
    assert solver.get_solution()[1] == solution_str


def test_sudoku_solver_records_stats():
    # Creiamo un puzzle semplice (9x9 con una cella vuota)
    grid = solved_grid(9)
    grid[0][0] = 0
    puzzle_str = prepare_string_from_grid(grid)

    solver = SudokuSolver(puzzle_str)
    solver.solve()

    # Verifichiamo che le statistiche siano state popolate
    # expanded_nodes dovrebbe essere almeno 1 (per la cella riempita)
    assert solver.expanded_nodes >= 1
    # max_memory_nodes rappresenta la profondità massima della ricorsione
    assert solver.max_memory_nodes >= 0

    # Nota: con 1 sola cella vuota, la Constraint Propagation 
    # potrebbe risolvere tutto prima di entrare nella ricorsione.
    print(f"\nNodes: {solver.expanded_nodes}, Depth: {solver.max_memory_nodes}")


def test_unsolvable_sudoku_returns_false():
    # Creiamo un puzzle impossibile (due 1 nella stessa riga)
    grid = solved_grid(9)
    grid[0][0] = 1
    grid[0][1] = 1
    puzzle_str = prepare_string_from_grid(grid)

    # Il solver dovrebbe accorgersi dell'errore o in fase di 
    # propagazione iniziale o durante il solve
    solver = SudokuSolver(puzzle_str)
    assert solver.solve() is False