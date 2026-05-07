"""Tests for the module-level helper functions in main.py."""

import math
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from main import load_puzzles, run_benchmark


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_puzzle_str(grid_size: int) -> str:
    """Return a minimal solved-puzzle string (all 1s in a legal pattern)."""
    block = int(math.isqrt(grid_size))
    grid = [
        [((r * block + r // block + c) % grid_size) + 1 for c in range(grid_size)]
        for r in range(grid_size)
    ]
    chars = []
    for row in grid:
        for val in row:
            if val <= 9:
                chars.append(str(val))
            else:
                chars.append(chr(val - 10 + ord('A')))
    return "".join(chars)


# ---------------------------------------------------------------------------
# load_puzzles
# ---------------------------------------------------------------------------

def test_load_puzzles_returns_none_when_csv_missing():
    """load_puzzles should return None when the CSV file cannot be loaded."""
    with patch("main.load_csv", return_value=None):
        result = load_puzzles(9)
    assert result is None


def test_load_puzzles_returns_none_when_column_missing():
    """load_puzzles should return None when the expected column is absent."""
    import pandas as pd
    dummy_df = pd.DataFrame({"wrong_column": ["abc"]})
    with patch("main.load_csv", return_value=dummy_df):
        result = load_puzzles(9)
    assert result is None


def test_load_puzzles_returns_list_on_success():
    """load_puzzles should return a list of strings on a valid DataFrame."""
    import pandas as pd
    puzzle = _make_puzzle_str(9)
    dummy_df = pd.DataFrame({"quizzes": [puzzle, puzzle]})
    with patch("main.load_csv", return_value=dummy_df):
        result = load_puzzles(9)
    assert isinstance(result, list)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# run_benchmark
# ---------------------------------------------------------------------------

def test_run_benchmark_random_mode_completes(capsys):
    """run_benchmark in Random mode should print a summary without errors."""
    puzzle = _make_puzzle_str(9)
    puzzles = [puzzle] * 5

    run_benchmark(puzzles, n=3, mode="R", grid_size=9)

    captured = capsys.readouterr()
    assert "BENCHMARK SUMMARY" in captured.out
    assert "Mean time" in captured.out
    assert "Valid solutions" in captured.out


def test_run_benchmark_static_mode_completes(capsys):
    """run_benchmark in Static mode should print a summary without errors."""
    puzzle = _make_puzzle_str(9)
    puzzles = [puzzle]

    run_benchmark(puzzles, n=2, mode="S", grid_size=9)

    captured = capsys.readouterr()
    assert "BENCHMARK SUMMARY" in captured.out
    assert "Static" in captured.out


def test_run_benchmark_empty_dataset_prints_error(capsys):
    """run_benchmark with an empty puzzle list should print an error."""
    run_benchmark([], n=3, mode="R", grid_size=9)
    captured = capsys.readouterr()
    assert "empty" in captured.out.lower()


def test_run_benchmark_random_mode_caps_n(capsys):
    """run_benchmark should not request more puzzles than are available."""
    puzzle = _make_puzzle_str(9)
    puzzles = [puzzle] * 2

    # n=10 but only 2 puzzles available — should not raise
    run_benchmark(puzzles, n=10, mode="R", grid_size=9)
    captured = capsys.readouterr()
    assert "BENCHMARK SUMMARY" in captured.out


def test_run_benchmark_reports_correct_grid_size(capsys):
    """Summary must display the correct grid size."""
    puzzle = _make_puzzle_str(9)
    run_benchmark([puzzle], n=1, mode="S", grid_size=9)
    assert "9x9" in capsys.readouterr().out
