"""Tests for the module-level helper functions in main.py."""


from unittest.mock import  patch
import pandas as pd

from main import load_puzzles_df, run_benchmark

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_puzzle_str(grid_size: int) -> str:
    """Return a minimal solved-puzzle string (all 1s in a legal pattern)."""
    # Usiamo una stringa di soli '1' o altri caratteri per simulare un puzzle
    # In un test reale, SudokuSolver proverà a risolverlo.
    return "1" * (grid_size * grid_size)

def _get_dummy_df(grid_size: int, rows: int = 2):
    """Crea un DataFrame fake con le colonne corrette per 9x9 o 16x16."""
    puzzle = _make_puzzle_str(grid_size)
    if grid_size == 9:
        return pd.DataFrame({"quizzes": [puzzle] * rows, "solutions": [puzzle] * rows})
    else:
        return pd.DataFrame({"Sudoku": [puzzle] * rows, "solution": [puzzle] * rows})

# ---------------------------------------------------------------------------
# load_puzzles_df
# ---------------------------------------------------------------------------

def test_load_puzzles_df_returns_none_when_csv_missing():
    """load_puzzles_df should return None when the CSV file cannot be loaded."""
    with patch("main.load_csv", return_value=None):
        result = load_puzzles_df(9)
    assert result is None

def test_load_puzzles_df_returns_dataframe_on_success():
    """load_puzzles_df should return a pandas DataFrame."""
    dummy_df = _get_dummy_df(9)
    with patch("main.load_csv", return_value=dummy_df):
        result = load_puzzles_df(9)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

# ---------------------------------------------------------------------------
# run_benchmark
# ---------------------------------------------------------------------------

def test_run_benchmark_random_mode_completes(capsys):
    """run_benchmark in Random mode should print a summary without errors."""
    df = _get_dummy_df(9, rows=5)

    # Mockiamo verify_sudoku_solution per evitare di far girare il solver reale
    # Restituisce: (is_correct, nodes, memory)
    with patch("main.verify_sudoku_solution", return_value=(True, 10, 5)):
        run_benchmark(df, n=3, mode="R", grid_size=9)

    captured = capsys.readouterr()
    assert "RIEPILOGO BENCHMARK" in captured.out
    assert "Soluzioni Valide" in captured.out
    assert "Nodi Medi Espansi" in captured.out

def test_run_benchmark_static_mode_completes(capsys):
    """run_benchmark in Static mode should print a summary without errors."""
    df = _get_dummy_df(9, rows=1)

    with patch("main.verify_sudoku_solution", return_value=(True, 10, 5)):
        run_benchmark(df, n=2, mode="S", grid_size=9)

    captured = capsys.readouterr()
    assert "RIEPILOGO BENCHMARK" in captured.out
    assert "9x9" in captured.out

def test_run_benchmark_empty_dataset_prints_error(capsys):
    """run_benchmark with an empty DataFrame should print an error."""
    empty_df = pd.DataFrame()
    run_benchmark(empty_df, n=3, mode="R", grid_size=9)
    captured = capsys.readouterr()
    assert "vuoto" in captured.out.lower()

def test_run_benchmark_reports_correct_metrics(capsys):
    """Verifica che le nuove metriche (nodi e memoria) appaiano nel riepilogo."""
    df = _get_dummy_df(16, rows=1)

    # Mock con valori specifici per testare i calcoli
    with patch("main.verify_sudoku_solution", return_value=(True, 100, 20)):
        run_benchmark(df, n=1, mode="R", grid_size=16)

    out = capsys.readouterr().out
    assert "100.00" in out  # Media nodi
    assert "20" in out      # Memoria massima
    assert "16x16" in out