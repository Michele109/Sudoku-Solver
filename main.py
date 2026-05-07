"""
Interactive benchmarking entry point for the Sudoku Solver project.

Supports both 9x9 (Standard) and 16x16 (Hexadoku) puzzles.
"""

import copy
import random
import time

import numpy as np

from src.solver.backtraking import solve_sudoku
from src.utils.loaders import load_csv
from src.utils.validation import is_valid_solution, verify_integrity
from src.utils.visualizer import prepare_grid_from_string

# Paths to the puzzle datasets
DATA_PATH_9x9 = "data/9x9sudoku.csv"
DATA_PATH_16x16 = "data/16x16sudoku.csv"

# Map each supported grid size to its dataset path and puzzle column name
GRID_CONFIG = {
    9: {"path": DATA_PATH_9x9, "column": "quizzes"},
    16: {"path": DATA_PATH_16x16, "column": "Sudoku"},
}


def prompt_grid_size() -> int:
    """Prompt the user to choose between 9x9 and 16x16."""
    while True:
        raw = input("Select grid size — enter 9 (Standard) or 16 (Hexadoku): ").strip()
        if raw in ("9", "16"):
            return int(raw)
        print("  Invalid input. Please enter 9 or 16.")


def prompt_sample_size() -> int:
    """Prompt the user for the number of puzzle instances to process."""
    while True:
        raw = input("Enter the number of puzzles to process (n > 0): ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("  Invalid input. Please enter a positive integer.")


def prompt_execution_mode() -> str:
    """Prompt the user to choose random or static execution mode."""
    while True:
        raw = input(
            "Select execution mode — enter R (Random) or S (Static): "
        ).strip().upper()
        if raw in ("R", "S"):
            return raw
        print("  Invalid input. Please enter R or S.")


def load_puzzles(grid_size: int):
    """Load the puzzle dataset for the given grid size.

    Returns a list of puzzle strings, or None on failure.
    """
    config = GRID_CONFIG[grid_size]
    df = load_csv(config["path"])
    if df is None:
        return None
    column = config["column"]
    if column not in df.columns:
        print(f"Error: column '{column}' not found in dataset (available: {list(df.columns)}).")
        return None
    return df[column].tolist()


def run_benchmark(puzzles: list, n: int, mode: str, grid_size: int) -> None:
    """Execute the benchmark and print a statistical summary.

    Parameters
    ----------
    puzzles:   list of puzzle strings loaded from the dataset.
    n:         number of instances to process.
    mode:      'R' for random selection, 'S' for static (same puzzle, n runs).
    grid_size: 9 or 16.
    """
    if len(puzzles) == 0:
        print("Error: dataset is empty.")
        return

    # Select the puzzle(s) to solve
    if mode == "R":
        n = min(n, len(puzzles))
        selected = random.sample(puzzles, n)
    else:  # Static mode: pick one puzzle, repeat n times
        puzzle_str = random.choice(puzzles)
        selected = [puzzle_str] * n

    times = []
    valid_count = 0

    print(f"\nRunning {n} puzzle(s) on a {grid_size}x{grid_size} grid …\n")

    for i, puzzle_str in enumerate(selected, start=1):
        grid = prepare_grid_from_string(puzzle_str, grid_size)
        original_grid = copy.deepcopy(grid)

        start = time.perf_counter()
        solved = solve_sudoku(grid)
        elapsed = time.perf_counter() - start

        times.append(elapsed)

        if solved and verify_integrity(original_grid, grid):
            valid_count += 1
            status = "✓"
        else:
            status = "✗"

        print(f"  Puzzle {i:>4}: {elapsed:.4f}s  {status}")

    # Statistical summary
    times_arr = np.array(times)
    validation_pct = (valid_count / n) * 100

    print("\n" + "=" * 45)
    print("  BENCHMARK SUMMARY")
    print("=" * 45)
    print(f"  Grid size       : {grid_size}x{grid_size}")
    print(f"  Mode            : {'Random' if mode == 'R' else 'Static'}")
    print(f"  Puzzles run     : {n}")
    print(f"  Mean time       : {times_arr.mean():.4f}s")
    print(f"  Min  time       : {times_arr.min():.4f}s")
    print(f"  Max  time       : {times_arr.max():.4f}s")
    print(f"  Std  deviation  : {times_arr.std():.4f}s")
    print(f"  Valid solutions : {valid_count}/{n} ({validation_pct:.1f}%)")
    print("=" * 45)


def main() -> None:
    """Interactive entry point."""
    print("\n=== Sudoku Solver Benchmarking Suite ===\n")

    grid_size = prompt_grid_size()
    n = prompt_sample_size()
    mode = prompt_execution_mode()

    puzzles = load_puzzles(grid_size)
    if puzzles is None:
        print("Failed to load dataset. Exiting.")
        return

    run_benchmark(puzzles, n, mode, grid_size)


if __name__ == "__main__":
    main()
