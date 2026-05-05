from src.utils import visualizer
from src.utils import loaders

# Constants for data paths[cite: 2]
DATA_PATH9x9 = 'data/9x9sudoku.csv'
DATA_PATH16x16 = 'data/16x16sudoku.csv'


def test_prepare_grid_9x9():
    """Verify that a 9x9 Sudoku string is correctly converted to a grid."""
    # Load dataset[cite: 2]
    dataset = loaders.load_csv(DATA_PATH9x9)
    sample_str = dataset['quizzes'][0]

    # Process string into grid[cite: 2]
    grid = visualizer.prepare_grid_from_string(sample_str, GRID_SIZE=9)

    # Assertions: Verify the structure
    assert len(grid) == 9, "The 9x9 grid should have 9 rows."
    assert all(len(row) == 9 for row in grid), "Every row in 9x9 grid must have 9 columns."


def test_prepare_grid_16x16():
    """Verify that a 16x16 Sudoku string is correctly converted to a grid."""
    # Load dataset[cite: 2]
    dataset = loaders.load_csv(DATA_PATH16x16)
    sample_str = dataset['Sudoku'][0]

    # Process string into grid[cite: 2]
    grid = visualizer.prepare_grid_from_string(sample_str, GRID_SIZE=16)

    # Assertions
    assert len(grid) == 16, "The 16x16 grid should have 16 rows."
    assert all(len(row) == 16 for row in grid), "Every row in 16x16 grid must have 16 columns."


def test_print_sudoku_grid_execution():
    """Ensure the visualizer print function executes without errors."""
    dataset = loaders.load_csv(DATA_PATH9x9)
    sample_str = dataset['quizzes'][0]

    # We check if the function runs. If it raises an exception, pytest fails[cite: 1].
    # Since print functions usually return None, we verify that result.
    result = visualizer.print_sudoku_grid(sample_str, GRID_SIZE=9)
    assert result is None